
from datetime import timedelta, datetime
from logging import getLogger

from src.time_pars import get_real_datetime
from src.log_scripts import set_logger

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
    student_id = card['id']
    try:
        # Create a cursor
        cursor = connection.cursor()
        # Execute the query
        cursor.execute("SELECT datetime FROM Applications WHERE id = %s", (student_id,))
        # Fetch all the rows
        rows = cursor.fetchall()
        logger.debug('Количество карточек с id = %s в базе данных: %s', student_id, len(rows))
        if not rows:
            logger.debug('Карточки с id = %s не было в базе данных', student_id)
            return False
        else:
            logger.debug('Карточка с id = %s была в базе данных', student_id)
            return rows[0][0]
    except Exception as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()

def was_not_modified(card, connection):
    student_id = card['id']
    try:
        # Create a cursor
        cursor = connection.cursor()
        # Execute the query
        cursor.execute("SELECT * FROM Applications WHERE id = %s AND modified = 0", (student_id,))
        # Fetch all the rows
        rows = cursor.fetchall()
        logger.debug('Количество карточек с id = %s в базе данных: %s', student_id, len(rows))
        if not rows:
            logger.debug('Карточки с id = %s уже была изменена', student_id)
            return False
        else:
            datetime = get_date_time_from_sql(card, connection)
            if datetime:
                time = card['posted']
                if time == "None":
                    time = "01 января 00:00"
                dt_str, timestamp = get_real_datetime(time)
                if check_time_difference(datetime, dt_str, 2):
                    logger.debug('Карточка с id = %s не была изменена', student_id)
                    return True
                else:
                    logger.debug('Карточка с id = %s была изменена', student_id)
                    return False
            else:
                logger.error('Не смогли достать timedate form sql Карточка с id = %s не была изменена', student_id)
                return False
    except Exception as e:
        logger.error(f"Ошибка при работе с базой данных: {e}")
        connection.rollback()
        return False
    finally:
        cursor.close()
