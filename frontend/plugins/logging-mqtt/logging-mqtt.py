import configparser

def main():
    print(__name__)

def details():
    return {'name': "MQTT Logging",
            'section': 'logging',
            'version': "0.1alpha1",
            'description': "Log events with MQTT.",
    }

def configuration():
    data = {}
    return data

section = 'MQTT'
settings = ['broker_address',
            'broker_topic']
def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}
    
    for setting in settings:
        data[setting] = config.get(section,setting)
    return data
    
def run():
    data = configuration()
    return data
