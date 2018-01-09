import time
import json

def main():
    print(__name__)

def details():
    return {'name': "location-manual",
            'section': 'location',
            'version': 0.1,
            'description': "Manually set location of detector.",
    }

def configuration():
    data = {
        'name': 'CERN',
        'lon': 6.053166454,
        'lat': 46.233832398,
        'alt': 0,
        'err_lon_meter': 999,
        'err_lat_meter': 999,
        'err_alt_meter': 999,
        'update_time_string': '1970-01-01T00:00:00.000Z',
        '_internal_timestamp': time.time()
    }
    return data

def run():
    data = configuration()
    return data
