# /src/database/add_card_to_sql.py
from logging import getLogger
from constants.pathes import db_path
from sqlite3 import Error
from database.login_to_sql_server import login_to_sql_server
from src.time_pars.get_real_datetime import get_real_datetime
from src.log_scripts.set_logger import set_logger
from src.database.price_database import PricesDatabase
from src.parsing_card.pars_prices import parse_prices

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def add_card_to_sql(sql, card: dict):
    if card['id'] == "None":
        logger.error("Карточка с id = None не добавлена в базу данных")
        return False
    c = sql.cursor()
    time = card['posted']
    if time == "None":
        time = "01 января 00:00"
    dt_str, timestamp = get_real_datetime(time)
    # SQL-запрос для добавления данных в таблицу
    sqld = 'INSERT INTO Applications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    data = (card['url'], card['id'], card['vizited'], card['img1'], card['img2'], card['schedule'], card['class_description'], card['in_time'], card['price'], card['distant'], card['address'], card['price_all'], card['ot_do'], card['subject'], card['name'], card['school'], card['posted'], card['html'], timestamp, dt_str, "", card['modified'], timestamp)
    pd = PricesDatabase(sql)
    ot, do = parse_prices(card['ot_do'], card['price'])
    pd.add_price_range(card['id'], ot, do)
    try:
        # Выполнение запроса и сохранение изменений
        c.execute(sqld, data)
        logger.info('Карточка с id = %s добавлена в базу данных', card['id'])
        return c.lastrowid
    except Error as error:
        logger.error("Ошибка при выполнении запроса:", error)
        return False


def main():
    sql = login_to_sql_server(db_path)
    if sql is None:
        logger.error('Ошибка при подключении к базе данных')
        return False
    # Данные для добавления в таблицу
    card = {'url': 'https://example.com', 'id': 1, 'vizited': 0, 'img1': 'img1.jpg', 'img2': 'img2.jpg', 'schedule': 'Mon-Fri', 'class_description': 'Class description', 'in_time': '10:00', 'price': '10 USD', 'distant': 1, 'address': '123 Main St', 'price_all': '100 USD', 'ot_do': 'From 10 to 20 years old', 'subject': 'Math', 'name': 'John Doe', 'school': 1, 'posted': '2022-02-21', 'html': '<html>...</html>'}
    logger.info('adding card to sql')
    add_card_to_sql(sql, card)
    sql.commit()
    sql.close()
    #create_tables(db_path)
    #create_db(db_path, user_name, password)


if __name__ == '__main__':
    main()