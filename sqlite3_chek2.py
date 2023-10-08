from datetime import datetime
import sqlite3
import re  # для работы с регулярными выражениями

def fix_datetime_format(wrong_datetime):
    try:
        dt = datetime.strptime(wrong_datetime, '%d.%m.%Y %H:%M')
        print(f"Wrong datetime is {wrong_datetime}")
        fixed_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Fixed datetime is {fixed_datetime}")
        return fixed_datetime
    except Exception as e:
        print(f"Could not parse datetime {wrong_datetime} error: {e}")
        return wrong_datetime  # Если формат уже правильный или не может быть исправлен


# Подключаемся к SQLite базе данных
conn_sqlite = sqlite3.connect('files/repetitors_copy.db')
conn_sqlite.create_function("fix_datetime_format", 1, fix_datetime_format)
cursor_sqlite = conn_sqlite.cursor()

# Получаем список всех таблиц
cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_sqlite.fetchall()

# Регулярное выражение для проверки datetime
datetime_regex = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')

# Проходим по каждой таблице
for table in tables:
    table_name = table[0]
    cursor_sqlite.execute(f"PRAGMA table_info({table_name});")
    columns_info = cursor_sqlite.fetchall()
    
    column_names = [column[1] for column in columns_info]

    for column in columns_info:
        column_name = column[1]
        is_nullable = column[3]  # 1 = not null, 0 = nullable

        if is_nullable:
            cursor_sqlite.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL;")
            count = cursor_sqlite.fetchone()[0]
            if count > 0:
                print(f"Column {column_name} in table {table_name} should not contain NULL but contains {count} NULL values.")

    if 'id' in column_names:
        cursor_sqlite.execute(f"SELECT MAX(id), MIN(id) FROM {table_name};")
        max_id, min_id = cursor_sqlite.fetchone()
        if max_id is not None and min_id is not None:
            if max_id > 9223372036854775807 or min_id < -9223372036854775808:
                print(f"Values in 'id' column in table {table_name} are out of range for PostgreSQL bigint.")

    """# Если у нас есть колонка datetime с неверным форматом
    if 'datetime' in column_names:
        # Используем пользовательскую функцию SQL для исправления формата
        cursor_sqlite.execute(f"UPDATE {table_name} SET datetime = fix_datetime_format(datetime);")
        conn_sqlite.commit()  # Сохраняем изменения в базе данных"""

    if 'datetime' in column_names:
        cursor_sqlite.execute(f"SELECT datetime FROM {table_name};")
        datetimes = cursor_sqlite.fetchall()
        invalid_datetime = [dt for dt, in datetimes if not datetime_regex.match(dt)]
        if invalid_datetime:
            print(f"Invalid datetime format in {len(invalid_datetime)} rows in table {table_name}.")
            print("Examples of invalid datetime formats:", invalid_datetime[:2])

# Закрыть соединение с SQLite
conn_sqlite.close()
