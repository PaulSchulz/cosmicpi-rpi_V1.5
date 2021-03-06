'''
This program manages the connection to an attached detector.

Features:
    Configurable via ../config/CosmicPi.config
    Start and/or setup the selected detector
    Calibrate selected detector
    Store event and sensor data in an sqlite data base

This program uses the interface of the class detector.
Thus, new detectors should be added via subclassing detector.

'''
import serial
import time
import threading
import sqlite3
import copy
import datetime
from serial import SerialException
import configparser

import logging as log
log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO)


class detector():
    # vars that are the same for all detectors
    _db_keys = ["UTCUnixTime", "SubSeconds", "TemperatureC", "Humidity",
                     "AccelX", "AccelY", "AccelZ", "MagX", "MagY", "MagZ",
                     "Pressure", "Longitude", "Latitude"]
    _example_event_dict = {
        "UTCUnixTime": 0,
        "SubSeconds": 0.0,
        "TemperatureC": 0.0,
        "Humidity": 0.0,
        "AccelX": 0.0,
        "AccelY": 0.0,
        "AccelZ": 0.0,
        "MagX": 0.0,
        "MagY": 0.0,
        "MagZ": 0.0,
        "Pressure": 0.0,
        "Longitude": 0.0,
        "Latitude": 0.0
    }

    def __init__(self, detector_name, detector_version, sqlite_location):
        # vars local to one detector
        self._sqlite_location = sqlite_location
        self.detector_name = detector_name
        self.detector_version = detector_version
        self._read_out_lock = threading.Lock()
        self._db_conn = 0
        self._initilize_DB()
        self._detector_initilized = False

    def _initilize_DB(self):
        self._db_conn = sqlite3.connect(self._sqlite_location, timeout=60.0)
        cursor = self._db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events'")
        if cursor.fetchone() == None:
            cursor.execute('''CREATE TABLE Events
             (UTCUnixTime INTEGER, SubSeconds REAL, TemperatureC REAL, Humidity REAL, AccelX REAL,
              AccelY REAL, AccelZ REAL, MagX REAL, MagY REAL, MagZ REAL, Pressure REAL, Longitude REAL,
              Latitude REAL, DetectorName TEXT, DetectorVersion TEXT);''')
            self._db_conn.commit()

    def initzilize_detector(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def start(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def stop(self):
        raise NotImplementedError("Should be implemented in the subclass!")

    def _commit_event_dict(self, event_dict):
        cursor = self._db_conn.cursor()
        # compile what needs to be sent
        insert_vals = []
        insert_string = 'INSERT INTO Events VALUES (?,?'
        for key in self._db_keys:
            insert_vals.append(event_dict[key])
            insert_string += ',?'
        insert_string += ')'
        insert_vals.append(self.detector_name)
        insert_vals.append(self.detector_version)

        # send and commit the changes
        cursor.execute(insert_string, insert_vals)
        self._db_conn.commit()



class CosmicPi_V15(detector, threading.Thread):
    def __init__(self, serial_port, baud_rate, sqlite_location, timeout=10, enable_raw_output=False):
        detector.__init__(self, "CosmicPiV1.5", "1.5.1", sqlite_location)
        # todo: put the thread inheritance one higher
        threading.Thread.__init__(self)
        # initilize the needed data structures
        self._gps_ok = False
        self._event_dict = copy.deepcopy(self._example_event_dict)
        self._event_dict_confirmed = copy.deepcopy(self._example_event_dict)
        self._event_dict_confirmed.pop('SubSeconds')
        self._all_data_collected = False
        self._time_from_gps = datetime.datetime(2000, 1, 2, 3, 4, 5, tzinfo=None)
        # store init values
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        # setup the writing onto disk
        self.enable_raw_output = enable_raw_output
        self._ouput_file_handler = 0
        if self.enable_raw_output is True:
            self._ouput_file_handler = open("1-5_raw_output.log", 'w')
            # empty the output file
            self._ouput_file_handler.write(" ")

    def initzilize_detector(self):
        connected = False
        while connected == False:
            try:
                self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)
            except SerialException as e:
                log.error("Could not establish a serial connection! Retrying in 10 seconds. Printing exception:")
                log.error(e)
                time.sleep(10)
                continue;
            connected = True

    def start(self):
        # make sure we empty the confirmations, to force new ones
        for element in self._event_dict_confirmed:
            self._event_dict_confirmed[element] = False
        self._gps_ok = False
        self.run()

    def stop(self):
        # could be implemented like this: https://stackoverflow.com/a/15734837
        raise NotImplementedError("Should be implemented in the subclass!")

    def run(self):
        # create an artificial interrupt
        while True:
            event_bool = False
            # read lines from serial and parse them
            #log.info("Reading line")
            event_bool = self._read_parse_and_check_for_event()

            # when there is an event store it
            if event_bool:
                log.info("Submitting event, with unix timestamp: " + str(self._event_dict['UTCUnixTime']))
                self._commit_event_dict(self._event_dict)

    def _read_parse_and_check_for_event(self):
        # read a line and directly store it in the raw data
        try:
            line = self.ser.readline()
            log.debug("Waiting serial input bytes: " + str(self.ser.inWaiting()))
        except SerialException as e:
            log.critical("Received a SerialException while reading the serial port (somebody probably unplugged the damn cable!). Printing error:")
            log.critical(e)
            raise RuntimeError("The detector can not function without a serial connection.")
        line_str = str(line)
        if self.enable_raw_output is True:
            self._ouput_file_handler.write(line_str)

        # parsing
        try:
            # get output data_type
            data_type = line_str.split(':')[0]

            # check if we have the type in our event dict
            if data_type in self._event_dict.keys():
                # do a second sanity check
                if (not (line_str.count(';') == 1)):
                    return False
                data = line_str.split(':')[1].split(';')[0]
                self._event_dict[data_type] = float(data)
                # mark the value as recieved
                self._event_dict_confirmed[data_type] = True
                return False

            # check for gps
            if data_type == "PPS":
                gps_lock_sting = line_str.split(':')[2]
                gps_lock_sting = gps_lock_sting.split(';')[0]
                # sanity check
                if (len(gps_lock_sting) == 1):
                    self._gps_ok = bool(int(gps_lock_sting))
                    # increment the time as well (with that we should be on the safe side of having events at the right time)
                    self._event_dict['UTCUnixTime'] += 1
                return False

            # check for GPS stings
            gps_type = line_str.split(',')[0]
            # check for a date string
            # ToDo: Make this an actual regular expression for "\$[A-Z][A-Z]ZDA"
            if gps_type == "$GPZDA" or gps_type == "$GNZDA":
                # sanity check
                if not (line_str.count(',') == 6):
                    return False
                g_time_string = line_str.split(',')[1].split('.')[0]    # has format hhmmss
                hour = int(g_time_string[0:2])
                minute = int(g_time_string[2:4])
                second = int(g_time_string[4:6])
                day = int(line_str.split(',')[2])
                month = int(line_str.split(',')[3])
                year = int(line_str.split(',')[4])
                self._time_from_gps = datetime.datetime(year,
                                                        month,
                                                        day,
                                                        hour,
                                                        minute,
                                                        second,
                                                        tzinfo=None)
                self._event_dict['UTCUnixTime'] = (self._time_from_gps - datetime.datetime(1970,1,1)).total_seconds()
                self._event_dict_confirmed['UTCUnixTime'] = True
                tt = self._event_dict['UTCUnixTime']
                return False

            # check for a location string
            if gps_type == "$GPGGA":
                # sanity check
                if not (line_str.count(',') == 14):
                    return False
                # use this as documentation for the string: http://aprs.gids.nl/nmea/#gga
                lat = line_str.split(',')[2]
                lat = float(lat[0:2])
                minutes = line_str.split(',')[2]
                minutes = float(minutes[2:len(minutes)])
                lat += minutes / 60.
                if line_str.split(',')[3] == 'S':
                    lat = -lat
                lon = line_str.split(',')[4]
                lon = float(lon[0:3])
                minutes = line_str.split(',')[4]
                minutes = float(minutes[3:len(minutes)])
                lon += minutes / 60.
                if line_str.split(',')[5] == 'W':
                    lon = -lon

                self._event_dict['Latitude'] = lat
                self._event_dict_confirmed['Latitude'] = True
                self._event_dict['Longitude'] = lon
                self._event_dict_confirmed['Longitude'] = True
                return False


            #log.info(str(self._event_dict_confirmed))
            # do a pre check if we have all data for a full event stack
            if self._gps_ok == False:
                return False
            # Don't do this check at the moment, it is annoying for development
            #if not self._all_data_collected:
            #    for element in self._event_dict_confirmed:
            #        if bool(self._event_dict_confirmed[element]) == False:
            #            return False
            #    # if we arrive here we have enough data and the check is obsolete
            #    self._all_data_collected = True
            self._all_data_collected = True

            # check if we have an event
            if data_type == "Event":
                # sanity check
                if not( (line_str.count(':')==3) and (line_str.count(';')==1) ):
                    return False
                sub_sec_string = line_str.split(':')[2]
                sub_sec_string = sub_sec_string.split(';')[0]
                # check if we are using the old or new event format
                if sub_sec_string.count('/') == 0:
                    # this is the old format using the micros function, so we simply divide by 1000000.0
                    current_subSeconds = float(sub_sec_string) / 1000000.0
                elif sub_sec_string.count('/') == 1:
                    # this is the newer format and we need to divide the first number by the second one
                    divisors = sub_sec_string.split('/')
                    current_subSeconds = float(divisors[0]) / float(divisors[1])
                # make sure we are actually seeing something new
                if (self._event_dict['SubSeconds'] == current_subSeconds):
                    return False
                else:
                    self._event_dict['SubSeconds'] = current_subSeconds
                    return True
            return False
        except IndexError as e:
            log.warning("Omitting a line, due to: Error while accessing the result of splitting the following line:" + str(line_str))
            return False
        except ValueError as e:
            log.warning("Omitting a line, due to: Error while converting a number from the following line: " + str(line_str))
            return False

#det = detector("Test1", "TestVersion1", config_sqlite_location)
#det._commit_event_dict(det._example_event_dict)

# settings files
CONFIG_FILE = "../config/CosmicPi.config"

# read configuration
# Todo: Put the config parser into a propper class
# Todo: Implement proper error catching for configparser (e.g. non existent keys or file)
# read configuration
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
detector_class = config.get("Detector", "detector_class")
sqlite_location = config.get("Storage", "sqlite_location")

# instanciate up the requested detector
det = 0
if detector_class == "CosmicPi_V15":
    serial_port = config.get(detector_class, "serial_port")
    baud_rate = config.get(detector_class, "baud_rate")
    enable_raw_output = config.getboolean(detector_class, "enable_raw_output")
    det = CosmicPi_V15(serial_port, baud_rate, sqlite_location, enable_raw_output=enable_raw_output)
if det == 0:
    log.critical("Could not find the detector class: " + str(detector_class))

# start the detector
log.info("Detector init")
det.initzilize_detector()
log.info("Starting detector")
det.start()
