import configparser

def main():
    print(__name__)

def details():
    return {'name': "Cosmic Array Sensors",
            'section': 'sensors',
            'version': "0.1alpha1",
            'description': "Read data from Cosmic Array.",
    }

def configuration():
    data = {}
    return data

section = 'sensors-cosmic-array'
settings = []
def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}

    #for setting in settings:
    #    data[setting] = config.get(section,setting)
    data = configuration()
    return data

def run():
    data = configuration()
    return data
