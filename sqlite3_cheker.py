import sqlite3

def find_minus_one(db_path):
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Получаем список всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Проходим по каждой таблице
    for table in tables:
        table_name = table[0]
        # Получаем информацию о столбцах
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [column[1] for column in cursor.fetchall()]

        # Проходим по каждому столбцу
        for column in columns:
            query = f"SELECT * FROM {table_name} WHERE {column} = -1;"
            cursor.execute(query)

            results = cursor.fetchall()
            if results:
                print(f"Таблица {table_name}, колонка {column} содержит значения -1.")
                print("Соответствующие строки:")
                for row in results:
                    print(row)

    # Закрываем соединение с базой данных
    conn.close()

# Путь к вашей базе данных SQLite
db_path = "files/repetitors.db"
find_minus_one(db_path)
