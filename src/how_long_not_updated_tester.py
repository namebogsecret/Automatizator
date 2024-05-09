
from datetime import datetime
import subprocess

def read_time_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

def parse_time(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

def should_restart_service(stored_time):
    current_time = datetime.now()
    difference = current_time - stored_time
    return difference.total_seconds() > 5000

def restart_service(service_name):
    subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)

# Путь к файлу и название сервиса
file_path = '/root/Automatizator/last_update.txt'
service_name = 'my_program.service'

# Выполнение
stored_time_str = read_time_from_file(file_path)
stored_time = parse_time(stored_time_str)

if should_restart_service(stored_time):
    restart_service(service_name)
