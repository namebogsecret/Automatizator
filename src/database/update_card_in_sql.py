debug = True
# create_db.py
from logging import getLogger
from src.parsing_card.pars_prices import parse_prices
from src.database.price_database import PricesDatabase
from src.constants.pathes import db_path
from sqlite3 import Error
if debug:
    from src.database.login_to_sql_server import login_to_sql_server
from src.time_pars.get_real_datetime import get_real_datetime
from src.log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def update_card_in_sql(sql, card: dict):
    
    c = sql.cursor()
    time = card['posted']
    if time == "None":
        time = "01 января 00:00"
    dt_str, timestamp = get_real_datetime(time)
    # SQL-запрос для добавления данных в таблицу
    sqld = '''UPDATE Applications SET url=%s, vizited=%s, img1=%s, img2=%s, schedule=%s, class_description=%s, in_time=%s, price=%s, distant=%s, address=%s, price_all=%s, ot_do=%s, subject=%s, name=%s, school=%s, posted=%s, html=%s, datetime=%s, modified=%s, timestamp_last=%s WHERE id=%s'''
    data = (card['url'], card['vizited'], card['img1'], card['img2'], card['schedule'], card['class_description'], card['in_time'], card['price'], card['distant'], card['address'], card['price_all'], card['ot_do'], card['subject'], card['name'], card['school'], card['posted'], card['html'], dt_str, card['modified'], timestamp, card['id'])
    try:
        # Выполнение запроса и сохранение изменений
        c.execute(sqld, data)
        pd = PricesDatabase(sql)
        ot, do = parse_prices(card['ot_do'], card['price'])
        pd.add_price_range(card['id'], ot, do)
    
        logger.info('Карточка с id = %s обновлена', card['id'])
        return c.lastrowid
    except Error as error:
        logger.error("Ошибка при выполнении запроса: %s", error)
        sql.rollback()
        return False
    finally:
        c.close()
