# /src/database/is_modified.py
from datetime import timedelta, datetime
from logging import getLogger
from src.time_pars.get_real_datetime import get_real_datetime
from src.log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def check_time_difference(dt1, dt2, max_time=2):
    dt1 = datetime.strptime(dt1, '%d.%m.%Y %H:%M')
    dt2 = datetime.strptime(dt2, '%d.%m.%Y %H:%M')
    delta = abs(dt1 - dt2)
    max_difference = timedelta(hours=max_time)
    return delta <= max_difference

def get_date_time_from_sql(card, connection):
    id = card['id']
    # Create a cursor
    cursor = connection.cursor()
    # Execute the query
    cursor.execute("SELECT datetime FROM Applications WHERE id = ?", (id,))
    # Fetch all the rows
    rows = cursor.fetchall()
    logger.debug('Количество карточек с id = %s в базе данных: %s', id, len(rows))
    if rows == []:
        logger.debug('Карточки с id = %s не было в базе данных', id)
        cursor.close()
        return False
    else:
        logger.debug('Карточка с id = %s была в базе данных', id)
        cursor.close()
        return rows[0][0]

def was_not_modified(card, connection):
    id = card['id']
    # Create a cursor
    cursor = connection.cursor()
    # Execute the query
    cursor.execute("SELECT * FROM Applications WHERE id = ? AND modified = 0", (id,))
    # Fetch all the rows
    rows = cursor.fetchall()
    logger.debug('Количество карточек с id = %s в базе данных: %s', id, len(rows))
    if rows == []:
        logger.debug('Карточки с id = %s уже была изменена', id)
        cursor.close()
        return False
    else:
        datetime = get_date_time_from_sql(card, connection)
        if datetime != False:
            time = card['posted']
            if time == "None":
                time = "01 января 00:00"
            dt_str, timestamp = get_real_datetime(time)
            if check_time_difference(datetime, dt_str, 2):
                logger.debug('Карточка с id = %s не была изменена', id)
                cursor.close()
                return True
            else:
                logger.debug('Карточка с id = %s была изменена', id)
                cursor.close()
                return False
        else:
            logger.error('Не смогли достать timedate form sql Карточка с id = %s не была изменена', id)
            cursor.close()
            return False
