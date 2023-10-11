
import time
import paramiko

SSH_CONFIG = {
    'hostname': '194.135.22.213',
    'port': 22,
    'username': 'root',
    'key_filename': '~/.ssh/id_rsa',  # путь к вашему приватному ключу
}
LOCAL_PORT = 65432

def setup_tunnel():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    client.connect(**SSH_CONFIG)
    transport = client.get_transport()
    channel = transport.open_channel('direct-tcpip', ('localhost', 5432), ('localhost', LOCAL_PORT))
    return channel, client

while True:
    try:
        channel, client = setup_tunnel()
        print(f"Туннель установлен на порт {LOCAL_PORT}")
        while True:
            time.sleep(10)  # Тут может быть ваш код
    except Exception as e:
        print(f"Проблема с туннелем: {e}. Переустановка...")
        client.close()
