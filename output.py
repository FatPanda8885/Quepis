import log
import sys


def info_output(info):
    global status
    import config
    CONFIG = config.get_config()
    status = CONFIG.get('log', 'enable')  # bool
    if status:
        log.write_info(info)
    print("\033[0;32;40m[INFO]\033[0m"+info)

def error_output(error):
    global status
    import config
    CONFIG = config.get_config()
    status = CONFIG.get('log', 'enable')  # bool
    if status:
        log.write_error(error)
    print("\033[0;31;40m[ERROR]\033[0m"+error)
    sys.exit(1)

def warn_output(warn):
    global status
    import config
    CONFIG = config.get_config()
    status = CONFIG.get('log', 'enable')  # bool
    if status:
        log.write_warn(warn)
    print("\033[0;33;40m[WARN]\033[0m"+warn)

def __init__():
    log.setup()