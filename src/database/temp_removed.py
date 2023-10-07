from datetime import datetime
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

def add_temp_removed(id, sql, html:str):
    cursor = sql.cursor()
    cursor.execute("SELECT id FROM Students_temp_removed WHERE id = %s", (id,))
    try:
        # пробоуем получить id из базы данных
        id = cursor.fetchone()[0]
        logger.info("Студент с id = " + str(id) + " уже есть в базе данных")
    except Exception as e:
        # если не получилось, то добавляем
        logger.info("Студента с id = " + str(id) + " нет в базе данных. Error: %s", str(e))
        cursor.execute("INSERT INTO Students_temp_removed (id, timestamp) VALUES (%s, %s)", (id, datetime.now().timestamp()))
        logger.info("Студент с id = " + str(id) + " добавлен в базу отложенных")
        sql.commit()

def is_temp_removed(id, sql, time_delta=30):  # time_delta - время в днях
    cursor = sql.cursor()
    cursor.execute("SELECT timestamp FROM Students_temp_removed WHERE id = %s", (id,))
    try:
        # пробоуем получить id из базы данных
        timestamp = cursor.fetchone()[0]
        logger.info("Студент с id = " + str(id) + " уже есть в базе данных. timestamp: " + str(timestamp))
        
        stamp_now = datetime.now().timestamp()
        delta = stamp_now - timestamp
        if delta > time_delta * 60 * 60 * 24:
            cursor.execute("DELETE FROM Students_temp_removed WHERE id = %s", (id,))
            logger.info("Студент с id = " + str(id) + " удален из базы отложенных")
            sql.commit()
            return False
        logger.info("Студент с id = " + str(id) + " есть в базе отложенных")
        return True
    except Exception as e:
        logger.error("Студента с id = " + str(id) + " нет в базе отложенных. Error: %s", str(e))
        return False

def remove_temp_removed(id, sql):
    cursor = sql.cursor()
    cursor.execute("DELETE FROM Students_temp_removed WHERE id = %s", (id,))
    logger.info("Студент с id = " + str(id) + " удален из базы отложенных")
    sql.commit()
