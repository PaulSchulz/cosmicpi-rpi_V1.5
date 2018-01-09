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

def run():
    return {}
