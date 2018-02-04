import configparser

def main():
    print(__name__)

def details():
    return {'name': "Example Module Template",
            'section': 'example',
            'version': 0.1,
            'description': "Example module",
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

    #for setting in settings:
    #    data[setting] = config.get(section,setting)
    data = configuration()
    return data

def run():
    data = configuration()
    return data
