# /src/database/create_db.py
from logging import getLogger
from constants.pathes import db_path
from sqlite3 import connect, Error
from log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

user_name = "admin"
password = "admintest"

def create_db(file_path, user_name, password):
    conn = connect(file_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (user_name, password) VALUES (?, ?)", (user_name, password))
    conn.commit()
    conn.close()
    logger.info('База данных создана')

def create_tables(file_path):
    logger.info('Создание таблиц')
    conn = connect(file_path)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS Applications 
            (url TEXT, 
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            subject TEXT, 
            price REAL, 
            is_willing_to_travel TEXT, 
            location TEXT, 
            is_willing_to_remote TEXT, 
            suitable_time_options TEXT, 
            created_at TEXT, 
            updated_at TEXT, 
            expired_at TEXT, 
            is_suitable_for_response INTEGER, 
            is_response_sent INTEGER, 
            response_text TEXT, 
            is_chat_reply_received INTEGER, 
            is_lesson_started INTEGER, 
            lesson_time_options TEXT)''')
        logger.info('Таблица Applications создана')
    except Error as error:
        # Если произошла ошибка, выводим сообщение об ошибке
        logger.error("Ошибка при выполнении запроса 1:", error)

    # Создаем таблицу "Данные об ученике"
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS StudentData 
            (id INTEGER PRIMARY KEY, 
            student_name TEXT, 
            parent_name TEXT, 
            parent_phone_number TEXT, 
            student_phone_number TEXT)''')
        logger.info('Таблица StudentData создана')
    except Error as error:
        # Если произошла ошибка, выводим сообщение об ошибке
        logger.error("Ошибка при выполнении запроса 2:", error)

    # Создаем таблицу "Отчеты о проведенных занятиях"
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS LessonReports 
            (id INTEGER PRIMARY KEY, 
            application_id INTEGER, 
            date TEXT, 
            time TEXT, 
            is_attended INTEGER, 
            is_paid INTEGER, 
            FOREIGN KEY(application_id) REFERENCES Applications(id))''')
        logger.info('Таблица LessonReports создана')
    except Error as error:
        # Если произошла ошибка, выводим сообщение об ошибке
        logger.error("Ошибка при выполнении запроса 3:", error)
    conn.commit()
    conn.close()
    logger.info('Таблицы созданы')

def ater_table(file_path):
    logger.info('Создание таблиц')
    conn = connect(file_path)
    c = conn.cursor()
    c.execute('DROP TABLE Applications')
    logger.info('Таблица Applications удалена')
    c.execute('''CREATE TABLE Applications
            (url TEXT, 
            id INTEGER PRIMARY KEY, 
            vizited INTEGER,
            img1 TEXT, 
            img2 TEXT, 
            schedule TEXT, 
            class_description TEXT, 
            in_time TEXT, 
            price TEXT, 
            distant INTEGER, 
            address TEXT, 
            price_all TEXT, 
            ot_do TEXT, 
            subject TEXT, 
            name TEXT, 
            school TEXT, 
            posted TEXT,
            html TEXT)''')
    logger.info('Таблица Applications создана')
def main():
    logger.info('Создание базы данных')
    ater_table(db_path)
    #create_tables(db_path)
    #create_db(db_path, user_name, password)


if __name__ == '__main__':
    main()