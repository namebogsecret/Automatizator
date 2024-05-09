from logging import getLogger
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def get_student(connection, student_id):
    """
    Получить информацию о студенте по его ID.

    Args:
    - connection: объект соединения с базой данных.
    - student_id: уникальный идентификатор студента.

    Returns:
    - tuple: кортеж данных о студенте или None при отсутствии записи или ошибке.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM studentsdata WHERE id = %s", (student_id,))
            logger.info('Запрос выполнен')
            return cursor.fetchone()
    except Exception as error:
        logger.error("Ошибка при выполнении запроса: %s", error)
        connection.rollback()
        return None

def get_urls(connection, number_of_cards):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT url FROM Applications ORDER BY timestamp_last DESC LIMIT %s", (number_of_cards,))
            logger.info('Запрос выполнен')
            return cursor.fetchall()
    except Exception as error:
        logger.error("Ошибка при выполнении запроса: %s", error)
        connection.rollback()
        return None

def get_applications(connection, number_of_cards):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT url, ot_do, price FROM Applications 
                WHERE NOT EXISTS (
                    SELECT 1 FROM StudentsData WHERE StudentsData.id = Applications.id
                ) ORDER BY timestamp_last DESC LIMIT %s
            """, (number_of_cards,))
            logger.info('Запрос выполнен')
            return cursor.fetchall()
    except Exception as error:
        logger.error("Ошибка при выполнении запроса: %s", error)
        connection.rollback()
        return []