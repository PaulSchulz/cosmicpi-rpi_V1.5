import configparser

def main():
    print(__name__)

def details():
    return {'name': "WPA Supplicant Networking",
            'section': 'networking',
            'version': 0.1,
            'description': "Configure Wifi settings in WPA Supplicant",
    }

def configuration():
    return {'networks':
            [{'active': 'true',
              'essid': 'cosmic-array',
              'password': '12345678910'}]}

section = 'network-wpa-supplicant'
settings = []
def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}

    #    for setting in settings:
    #        data[setting] = config.get(section,setting)
    data = configuration()
    return data

def run():
    return {}
