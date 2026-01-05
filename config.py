import configparser

CONFIG = None

def setup():
    global CONFIG
    try:
        CONFIG = configparser.ConfigParser()
        CONFIG.read('config.ini', encoding='utf-8' )
    except Exception as e:
        raise e

def get_config():
    global CONFIG
    return CONFIG

