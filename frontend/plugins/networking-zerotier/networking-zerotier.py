import configparser

def main():
    print(__name__)

def details():
    return {'name': "ZeroTier Networking",
            'section': 'networking',
            'version': 0.1,
            'description': "Configure ZeroTier virtual network.",
    }

def configuration():
    return {'networks':
            [{'active': 'true',
              'id': '',
              }]}

section = 'template'
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
