"""
Модуль предоставляет класс SshTunnelCreator для создания и управления SSH-туннелями.
"""

from os import getenv
import time
from sshtunnel import SSHTunnelForwarder
import dotenv

dotenv.load_dotenv()

class SshTunnelCreator:
    """
    Класс sshtunnel_creator используется для создания и управления SSH-туннелем для перенаправления
    подключений на удаленный сервер.
    """

    def __init__(self):
        """
        Функция инициализирует словарь с параметрами конфигурации SSH и устанавливает логическую
        переменную в значение False.
        """
        self.ssh_config = {
            'ssh_address_or_host': (getenv("serv_host"), int(getenv("serv_port"))),
            'ssh_username': getenv("serv_user"),
            'ssh_pkey': getenv("serv_ssh_key_path"),  # путь к вашему приватному ключу
            'remote_bind_address': (getenv("serv_bind_host"), int(getenv("serv_bind_port"))),
        }
        self.tonnel_created = False
        self.tunnel = None
        self.local_port = None

    def create_tunnel(self):
        """
        Функция создает SSH-туннель и постоянно проверяет, работает ли туннель, и переподключается в
        случае возникновения проблем.
        """
        while True:
            with SSHTunnelForwarder(**self.ssh_config) as tunnel:
                self.tunnel = tunnel
                self.local_port = tunnel.local_bind_port
                self.tonnel_created = True
                print(f"Туннель установлен на порт {tunnel.local_bind_port}")
                try:
                    while self.tonnel_created:
                        time.sleep(60)  # Тут может быть ваш код
                        print("Туннель работает")
                    raise Exception("Туннель закрыт")
                except Exception as e:
                    print(f"Проблема с туннелем: {e}. Переустановка...")
                finally:
                    print("Соединение закрыто")

    def close_tunnel(self):
        """
        Функция close_tunnel проверяет, создан ли туннель, и закрывает его, если да,
        в противном случае печатает сообщение о том, что туннель не создан.
        """
        if self.tonnel_created:
            self.tonnel_created = False
            print("Закрываем туннель")
            self.tunnel.close()
        else:
            print("Туннель не создан")
