import socket
import re
import output
import config
import json

CONFIG = config.get_config()
socket_ip = CONFIG.get('game', 'ip')
socket_port = int(CONFIG.get('game', 'port'))
reason_list = []

def setup():
    global socket_ip, socket_port, socket_server, mode, reason_list
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.connect((socket_ip, socket_port))  # Connect to the existing server
        output.info_output("Successfully connected to the remote TCP server")
    except Exception as e:
        output.error_output(f"Failed to connect to the remote TCP server: {e}")
        raise e

    try:
        reason_str = CONFIG.get('unban', 'reason')
        reason_list = json.loads(reason_str)
        mode = CONFIG.get('unban', 'mode')
    except Exception as e:
        output.error_output(f"Failed to load unban reasons from config: {e}")
        raise e

def check_reason(reason):
    global unban_list,mode
    if mode == "blacklist":
        if reason in reason_list:
            return True
        else:
            return False
    elif mode == "whitelist":
        if reason in reason_list:
            return False
        else:
            return True
    else:
        output.error_output(f"Invalid unban mode in config: {mode}")
        return False

def unban(username):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((socket_ip, socket_port))
            s.send(f"unban {username}\n".encode('utf-8'))
        return True
    except Exception as e:
        print(f"Unban failed: {e}")
        return False