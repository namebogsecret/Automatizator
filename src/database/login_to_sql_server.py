# /src/database/login_to_sql_server.py
from logging import getLogger
from os import getenv
import psycopg2
#from psycopg2 import Error
#from psycopg2.extras import execute_values
import dotenv
from log_scripts.set_logger import set_logger

dotenv.load_dotenv()

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def login_to_postgres():
    try:
        connection = psycopg2.connect(
            dbname=getenv("dbname"),
            user=getenv("user"),
            password=getenv("password"),
            host=getenv("host")
        )
        return connection
    except psycopg2.OperationalError:  # Если ошибка связана с отсутствием базы данных
        # Попытка создать базу данных
            return None
    except Exception as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        return None