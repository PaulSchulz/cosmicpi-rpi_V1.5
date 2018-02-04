import configparser

import time
import requests
import json

def main():
    print(__name__)

def details():
    return {'name': "GeoIP Location (WIP)",
            'section': 'location',
            'version': 0.1,
            'description': "Find location via FreeGeoIP service.",
    }

section = 'location-geoip'
settings = ['url']

def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}
    
    #    for setting in settings:
    #        data[setting] = config.get(section,setting)

    # Defaults
    data['url'] = 'http://freegeoip.net/json'
    return data

def configuration():
    return {'url': 'http://freegeoip.net/json'}

def run():
    send_url = 'http://freegeoip.net/json'
    try:
        r = requests.get(send_url)
    except requests.exceptions.ConnectionError as e:
        #e = sys.exc_info()[0]
        #print(e)
        print("Unable to connect to the GeopIP-server!")
        print("Following ConnectionError occurred:", end='')
        print(e)
        print("Will retry in one minute.")
        time.sleep(60)
        return {}
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    data = {}
    data['lon'] = lon
    data['lat'] = lat
    data['alt'] = 0
    data['err_lon_meter'] = 500
    data['err_lat_meter'] = 500
    data['err_alt_meter'] = 500
    data['update_time_string'] = "NoTimeInGeoIP!"
    data['_internal_timestamp'] = time.time()
    # update our loc data

    return data

