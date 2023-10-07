from logging import getLogger
from sound.pik import pik
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

def update_students_data(url: str, sql, status: str, html: str, html_choose: str, html_otklik_param: str, all_text: str):
    logger.info("Обновление статуса студента в базе данных")
    logger.debug("Статус студента: " + status)
    logger.debug("URL: " + url)
    start_index = url.find('o=') + 2
    logger.debug("start_index: " + str(start_index))
    end_index = url.find('&', start_index)
    logger.debug("end_index: " + str(end_index))
    id = url[start_index:end_index]
    logger.debug("id: " + str(id))
    cursor = sql.cursor()
    cursor.execute("SELECT id FROM Applications WHERE id = %s", (id,))
    try:
        # пробоуем получить id из базы данных
        iddb = cursor.fetchone()[0]
        logger.info("Студент с id = " + str(iddb) + " уже есть в базе данных")
        cursor.execute("INSERT INTO StudentsData (id, status, html, html_choose, html_otklik_param, all_text) VALUES (%s, %s, %s, %s, %s, %s)", (iddb, status, html, html_choose, html_otklik_param, all_text))
        pik(100)
    except Exception as e:
        logger.error("Студента нет в базе данных. Error: %s", str(e))
    sql.commit()
    return True
