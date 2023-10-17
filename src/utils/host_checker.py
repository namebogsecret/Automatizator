
from os import name as os_name
import platform
import socket

def host_checker():
    hostname = socket.gethostname()
    system = platform.system()

    if hostname == "vladimir.local" or system == "Darwin" and os_name == "posix":
        return "local"
    if system == "Linux" or hostname == "ruvds-cq9bh" and os_name == "posix":
        return "server"
    else:
        return None
