import configparser

def main():
    print(__name__)

def details():
    return {'name': "AP Networking (WIP)",
            'section': 'networking',
            'version': '0.1alpha1',
            'description': "Run Wifi AP on detector to allow networking.",
    }

def configuration():
    data = {}
    return data

section = 'template'
settings = []
def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}

    #    for setting in settings:
    #        data[setting] = config.get(section,setting)
    return data

def run():
    data = configuration()
    return data
