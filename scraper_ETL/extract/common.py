import yaml

__config = None

def config():
    # Get access to global variable
    global __config

    # If we don't get the config yet...
    if not __config:
        with open('config.yaml', mode='r') as f:
            config = yaml.safe_load(f)

    return config

