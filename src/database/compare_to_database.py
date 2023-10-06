# /src/database/compare_to_database.py
from logging import getLogger
from src.log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def allready_in_db(id, connection):
    # Create a cursor
    cursor = connection.cursor()
    # Execute the query
    cursor.execute("SELECT * FROM Applications WHERE id = ?", (id,))
    # Fetch all the rows
    rows = cursor.fetchall()
    logger.debug('Количество карточек с id = %s в базе данных: %s', id, len(rows))
    if rows == []:
        logger.debug('Карточки с id = %s нет в базе данных', id)
        cursor.close()
        return False
    else:
        logger.debug('Карточка с id = %s есть в базе данных', id)
        cursor.close()
        return True

def compare_to_database(card, connection):
    # Create a cursor
    if allready_in_db(card["id"], connection):
        logger.debug('Карточка с id = %s есть в базе данных', card["id"])
        return 1
    else:
        logger.debug('Карточки с id = %s нет в базе данных', card["id"])
        return 0
