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

def run():
    return {}
