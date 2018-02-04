import configparser

def main():
    print(__name__)

def details():
    return {'name': "Cosmic Array Logging (WIP)",
            'section': 'logging',
            'version': "0.1alpha1",
            'description': "Log event data to the Cosmic Array network.",
    }

def configuration():
    data = {'destination': 'log.cosmic-array'}
    return data

section = 'logging-cosmic-array'
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
    data = configuration()
    return data
