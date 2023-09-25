#/src/database/update_card_in_sql.py
debug = True
# create_db.py
from logging import getLogger
from parsing_card.pars_prices import parse_prices
from database.price_database import PricesDatabase
from constants.pathes import db_path
from sqlite3 import Error
if debug:
    from database.login_to_sql_server import login_to_sql_server
from time_pars.get_real_datetime import get_real_datetime
from log_scripts.set_logger import set_logger
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
    sqld = 'UPDATE Applications SET url=?, vizited=?, img1=?, img2=?, schedule=?, class_description=?, in_time=?, price=?, distant=?, address=?, price_all=?, ot_do=?, subject=?, name=?, school=?, posted=?, html=?, datetime=?, modified=?, timestamp_last=? WHERE id=?'
    data = (card['url'], card['vizited'], card['img1'], card['img2'], card['schedule'], card['class_description'], card['in_time'], card['price'], card['distant'], card['address'], card['price_all'], card['ot_do'], card['subject'], card['name'], card['school'], card['posted'], card['html'], dt_str, card['modified'], card['id'], timestamp)
    try:
        # Выполнение запроса и сохранение изменений
        c.execute(sqld, data)
        pd = PricesDatabase(sql)
        ot, do = parse_prices(card['ot_do'], card['price'])
        pd.add_price_range(card['id'], ot, do)
    
        logger.info('Карточка с id = %s обновлена', card['id'])
        return c.lastrowid
    except Error as error:
        logger.error("Ошибка при выполнении запроса:", error)
        return False