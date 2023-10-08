from psycopg2 import connect, extensions
from logging import getLogger
from log_scripts.set_logger import set_logger



# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)
class PricesDatabase:
    def __init__(self, con: extensions.connection):
        self.conn = con
        self.cur = self.conn.cursor()
        self.create_table()

    def __del__(self):
        self.cur.close()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS prices (
                id SERIAL PRIMARY KEY,
                ot INTEGER,
                ido INTEGER
            )
        ''')
        logger.info('Таблица prices создана')
        self.conn.commit()

    def add_price_range(self, id, ot, ido):
        if not self.check_prices_exists(id):
            self.cur.execute("UPDATE prices SET ot=%s, ido=%s WHERE id=%s", (ot, ido, id,))
            logger.info('Диапазон цен обновлен в базе данных')
            return False
        self.cur.execute("INSERT INTO prices (id, ot, ido) VALUES (%s, %s, %s)", (id, ot, ido,))
        logger.info('Диапазон цен добавлен в базу данных')
        self.conn.commit()
        return True

    def get_price_range_by_id(self, price_id):
        if not self.check_prices_exists(price_id):
            return None
        self.cur.execute("SELECT ot, ido FROM prices WHERE id=%s", (price_id,))
        logger.info('Диапазон цен получен из базы данных')
        return self.cur.fetchone()

    def delete_price_range_by_id(self, price_id):
        self.cur.execute("DELETE FROM prices WHERE id=%s", (price_id,))
        self.conn.commit()
        logger.info('Диапазон цен удален из базы данных')
        return True

    def get_price_ranges_by_price(self, price):
        self.cur.execute("SELECT * FROM prices WHERE %s BETWEEN ot AND ido", (price,))
        logger.info('Диапазоны цен получены из базы данных')
        return self.cur.fetchall()
    
    def check_prices_exists(self, id):
        try:
            self.cur.execute("SELECT * FROM prices WHERE id = %s", (id,))
            logger.info('Проверка наличия диапазона цен в базе данных')
        except Exception as e:
            logger.error(f"Ошибка при работе с базой данных: {e}")
            return False
        result = self.cur.fetchone()
        return bool(result)
