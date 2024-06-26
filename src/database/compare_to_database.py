from logging import getLogger
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def allready_in_db(id, connection):
    try:
        if id is None:
            logger.error("Передано None в качестве идентификатора")
            return False
        # Create a cursor
        cursor = connection.cursor()
        # Execute the query
        cursor.execute("SELECT * FROM Applications WHERE id = %s", (id,))
        # Fetch all the rows
        rows = cursor.fetchall()
        logger.debug('Количество карточек с id = %s в базе данных: %s', id, len(rows))
        return len(rows) > 0
    except Exception as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        connection.rollback()  # Откатываем транзакцию при возникновении ошибки
        return False
    finally:
        cursor.close()  # Закрываем курсор

def compare_to_database(card, connection):
    if card is None:
        logger.error("Передан None в качестве карточки")
        return 0
    if "id" not in card or card["id"] is None:
        logger.error("Отсутствует id в карточке или он равен None")
        return 0
    logger.debug(str(card))
    if allready_in_db(card["id"], connection):
        logger.debug('Карточка с id = %s есть в базе данных', card["id"])
        return 1
    else:
        logger.debug('Карточки с id = %s нет в базе данных', card["id"])
        return 0
