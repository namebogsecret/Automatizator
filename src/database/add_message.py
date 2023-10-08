
from logging import getLogger
from typing import Any
import psycopg2
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def add_message(connection, uchenik_id: int, answer_text: str, timestamp: float, dur: float, temp:float) -> None:
    """
    Добавляет сообщение в таблицу gpt в PostgreSQL базу данных.
    
    Args:
        connection (obj): Объект соединения с PostgreSQL базой данных.
        uchenik_id (int): ID ученика.
        answer_text (str): Текст ответа.
        timestamp (float): Временная метка.
        dur (float): Продолжительность.
        temp (float): Температура.
        
    Returns:
        None
    """
    
    try:
        # Создать курсор для выполнения SQL запросов
        cursor = connection.cursor()
        
        # SQL запрос для добавления записи
        add_message_query = """
        INSERT INTO gpt (id, answer, timestamp, duration, temperature)
        VALUES (%s, %s, %s, %s, %s);
        """
        
        # Выполнить SQL запрос
        cursor.execute(add_message_query, (uchenik_id, answer_text, timestamp, dur, temp))
        logger.info('Сообщение добавлено в базу данных')
        # Зафиксировать изменения
        connection.commit()
        
    except Exception as e:
        logger.error("Ошибка при выполнении запроса: %s", e)
        connection.rollback()
        return False
    finally:
        cursor.close()