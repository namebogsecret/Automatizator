# /src/database/login_to_sql_server.py
from logging import getLogger
from sqlite3 import connect, Error
from src.log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

#login to sql server with credentials
def login_to_sql_server(path_to_sql_file):
    # Create a connection to the database
    try:
        connection = connect(path_to_sql_file)
        logger.info("Подключение к базе данных прошло успешно")
    except Error as error:
        logger.error("Ошибка при подключении к базе данных: %s", error)
        connection = None
    # Return the connection
    return connection