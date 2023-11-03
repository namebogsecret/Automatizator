import os
import platform
import socket

hostname = socket.gethostname()
system = platform.system()

if hostname == "vladimir.local" or system == "Darwin" and os.name == "posix":
    print("local")
elif system == "Linux" or hostname == "ruvds-cq9bh" and os.name == "posix":
    print("server")
else:
    print("Ошибка определения платформы")
