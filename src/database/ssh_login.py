"""
Подлкючение к БД через SSH
"""

from os import getenv
from psycopg2 import connect
import dotenv

dotenv.load_dotenv()

class SshDbConnector:
    """
    Класс SshDbConnector предоставляет методы для подключения к базе данных PostgreSQL
    через SSH.
    """
    def __init__(self, local_port):
        self.host = getenv("post_serv_host")
        self.user = getenv("post_serv_user ")
        self.password = getenv("post_serv_password")
        self.dbname = getenv("post_serv_dbname")
        self.port = local_port
        self.conn = None
                
    def db_connect(self):
        self.conn = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            dbname=self.dbname,
            port=self.port
        )
        while not self.conn:
            continue
        return self.conn
    
    def is_connected(self):
        return self.conn is not None

    def close(self):
        self.conn.close()
    
    def execute(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            yield rows
    
    def execute_with_commit(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()
