
from typing import Any
import psycopg2

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
        
        # Зафиксировать изменения
        connection.commit()
        
    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()