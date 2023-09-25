from sqlite3 import Connection, Error, connect
from typing import Any

def add_message(conn: Connection, uchenik_id: int, answer_text: str, timestamp: float, dur: float, temp:float) -> None:
    """
    Добавляет сообщение в таблицу gpt в SQLite базу данных.
    
    Args:
        db_path (str): Путь к SQLite базе данных.
        uchenik_id (Any): ID ученика.
        answer_text (str): Текст ответа.
        timestamp (float): Временная метка.
        
    Returns:
        None
    """
    
    try:
        # Создать курсор для выполнения SQL запросов
        cursor = conn.cursor()
        
        # SQL запрос для добавления записи
        add_message_query = """
        INSERT INTO gpt (id, answer, timestamp, duration, temperature)
        VALUES (?, ?, ?, ?, ?);
        """
        
        # Выполнить SQL запрос
        cursor.execute(add_message_query, (uchenik_id, answer_text, timestamp, dur, temp))
        
        # Зафиксировать изменения
        conn.commit()
        
    except Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        
    finally:
        # Закрыть соединение с базой данных
        pass



if __name__ == "__main__":
    # Пример использования
    #db_path = "your_database.db"
    uchenik_id = 1
    answer_text = "Привет, это GPT-4."
    timestamp = 1632234523.0
    dur = 0.0
    temp = 0.0
    from os.path import join
    db_path = join('files', 'repetitors.db')
    #sql = login_to_sql_server(db_path)
    #add_message(sql, uchenik_id, answer_text, timestamp, dur, temp)
