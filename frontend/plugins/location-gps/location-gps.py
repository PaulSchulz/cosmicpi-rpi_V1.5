import configparser

import time
import json

def main():
    print(__name__)

def details():
    return {'name': "GPS Location (WIP)",
            'section': 'location',
            'version': 0.1,
            'description': "Find location via local GPS service.",
    }

section = 'location-gps'
settings = []

def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    data = {}
    
    #    for setting in settings:
    #        data[setting] = config.get(section,setting)
    return data

def configuration():
    return {'port': ''}

def run():
    data = {}
    return data

