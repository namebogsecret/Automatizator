from os.path import join as os_join
from os import listdir
from re import search as re_search
from sqlite3 import connect, Error, Connection

from add_message import add_message

def read_and_add_messages_to_db(conn: Connection, answers_folder: str) -> None:
    
    for filename in listdir(answers_folder):
        filepath = os_join(answers_folder, filename)
        
        # Разбираем имя файла
        if filename.startswith('answer_'):
            """parts = filename.split('_')
            uchenik_id = int(parts[1])
            timestamp = float(parts[2].split('.')[0])
            
            with open(filepath, 'r') as f:
                lines = f.readlines()
                
                # Извлекаем дополнительную информацию и текст ответа
                first_line = lines[0].strip() #
                duration_temp = re_search(r'Время запроса: (.+)c. temp = (.+).', first_line) # 
                duration = float(duration_temp.group(1))
                temperature = float(duration_temp.group(2))
                
                answer_text = ' '.join(lines[1:]).strip()
                
                # Добавляем в базу данных
                add_message(conn, uchenik_id, answer_text, timestamp, duration, temperature)"""
                
        elif filename.startswith('dop_info_'):
            parts = filename.split('_')
            uchenik_id = int(parts[2])
            timestamp = float(parts[3].split('.')[0])
            
            with open(filepath, 'r') as f:
                answer_text = f.read().strip()
                
                # Добавляем в базу данных без duration и temperature
                add_message(conn, uchenik_id, answer_text, timestamp, None, None)
                
    # Закрыть соединение с базой данных
    #conn.close()
def login_to_sql_server(path_to_sql_file):
    # Create a connection to the database
    try:
        connection = connect(path_to_sql_file)
    except Error as error:
        print("Ошибка при подключении к базе данных:", error)
        connection = None
    # Return the connection
    return connection

if __name__ == "__main__":
    # Путь к вашей папке с ответами и к базе данных
    answers_folder = "answers"
    db_path = os_join('files', 'repetitors.db')
    sql = login_to_sql_server(db_path)
    # Вызываем функцию
    read_and_add_messages_to_db(sql, answers_folder)
