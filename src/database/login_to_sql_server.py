# /src/database/login_to_sql_server.py
from logging import getLogger
from os import getenv
import psycopg2
import dotenv

from src.log_scripts import set_logger

dotenv.load_dotenv()

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def login_to_sql_server():
    try:
        connection = psycopg2.connect(
            dbname=getenv("dbname"),
            user=getenv("dbuser"),
            password=getenv("dbpassword"),
            host=getenv("dbhost")
        )
        #logger.info("Подключение к базе данных прошло успешно")
        return connection
    except psycopg2.OperationalError:  # Если ошибка связана с отсутствием базы данных
        # Попытка создать базу данных
        logger.error("База данных не найдена. Попытка создать базу данных (no)")
        return None
    except Exception as e:
        logger.error(f"Ошибка при подключении к базе данных: {e}")
        return None
    
if __name__ == "__main__":
    login_to_sql_server()