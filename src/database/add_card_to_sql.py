# /src/database/add_card_to_sql.py
from logging import getLogger
from constants.pathes import db_path
from database.login_to_sql_server import login_to_sql_server
from time_pars.get_real_datetime import get_real_datetime
from log_scripts.set_logger import set_logger
from database.price_database import PricesDatabase
from parsing_card.pars_prices import parse_prices

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def add_card_to_sql(connection, card: dict):
    if card['id'] == "None":
        logger.error("Карточка с id = None не добавлена в базу данных")
        return False
    
    time = card['posted']
    if time == "None":
        time = "01 января 00:00"
    dt_str, timestamp = get_real_datetime(time)
    if card['modified'] == "":
        card['modified'] = None
    # SQL-запрос для добавления данных в таблицу
    sqld = '''INSERT INTO Applications 
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    data = (card['url'], card['id'], card['vizited'], card['img1'], card['img2'], card['schedule'], 
            card['class_description'], card['in_time'], card['price'], card['distant'], card['address'], 
            card['price_all'], card['ot_do'], card['subject'], card['name'], card['school'], card['posted'], 
            card['html'], timestamp, dt_str, "", card['modified'], timestamp)

    try:
        pd = PricesDatabase(connection)
        ot, do = parse_prices(card['ot_do'], card['price'])
        pd.add_price_range(card['id'], ot, do)
        logger.info('Диапазон цен добавлен в базу данных')
    except Exception as error:
        logger.error("Ошибка при добавлении диапазона цен: %s", error)
        return False

    try: 
        cursor = connection.cursor()
        cursor.execute(sqld, data)
        #added_card_id = cursor.fetchone()[0]
        connection.commit()
        logger.info('Карточка с id = %s добавлена в базу данных', card['id'])
        #return cursor.fetchone()[0]
        #return added_card_id
        return True
    except Exception as error:
        logger.error("Ошибка при выполнении запроса: %s", error)
        connection.rollback()
        return False
    finally:
        cursor.close()


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