from logging import getLogger
from psycopg2 import extensions
from src.log_scripts.set_logger import set_logger



# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)
# Класс PricesDatabase — это класс Python, который предоставляет методы для управления диапазонами цен
# в базе данных.
class PricesDatabase:
    def __init__(self, con: extensions.connection):
        """
        Функция инициализирует экземпляр класса объектом соединения и создает таблицу в базе данных.
        
        :param con: Параметр con имеет тип extensions.connection. Вполне вероятно, что «расширения» —
        это модуль или пакет, предоставляющий объект подключения для взаимодействия с базой данных.
        Параметр con используется для передачи экземпляра этого объекта соединения методу __init__
        :type con: extensions.connection
        """
        self.conn = con
        self.cur = self.conn.cursor()
        self.create_table()

    def __del__(self):
        """
        Вышеуказанная функция представляет собой метод деструктора, который закрывает курсор базы
        данных.
        """
        self.cur.close()

    def create_table(self):
        """
        Функция создает таблицу с именем «цены» с тремя столбцами (id, ot, ido), если она еще не
        существует.
        """
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
        """
        Функция add_price_range обновляет или вставляет диапазон цен в таблицу базы данных.
        
        :param id: Параметр «id» используется для идентификации конкретного ценового диапазона в базе
        данных. Вероятно, это уникальный идентификатор для каждого ценового диапазона
        :param ot: Параметр «ot» в коде представляет собой начальную цену ценового диапазона
        :param ido: Параметр «ido» представляет собой верхнюю границу ценового диапазона
        :return: логическое значение. Он возвращает True, если диапазон цен был успешно добавлен в базу
        данных, и False, если диапазон цен уже существует в базе данных.
        """
        if self.check_prices_exists(id):
            self.cur.execute("UPDATE prices SET ot=%s, ido=%s WHERE id=%s", (ot, ido, id,))
            logger.info('Диапазон цен обновлен в базе данных')
            self.conn.commit()
            return False
        self.cur.execute("INSERT INTO prices (id, ot, ido) VALUES (%s, %s, %s)", (id, ot, ido,))
        logger.info('Диапазон цен добавлен в базу данных')
        self.conn.commit()
        return True

    def get_price_range_by_id(self, price_id):
        """
        Функция извлекает диапазон цен из базы данных на основе заданного идентификатора цены.
        
        :param price_id: Параметр Price_id — это идентификатор ценового диапазона, который вы хотите
        получить из базы данных. Он используется для запроса таблицы цен и получения соответствующего
        диапазона цен
        :return: кортеж, содержащий значения столбцов «ot» и «ido» из таблицы «prices» в базе данных.
        """
        if not self.check_prices_exists(price_id):
            return None
        self.cur.execute("SELECT ot, ido FROM prices WHERE id=%s", (price_id,))
        logger.info('Диапазон цен получен из базы данных')
        return self.cur.fetchone()

    def delete_price_range_by_id(self, price_id):
        """
        Функция удаляет диапазон цен из базы данных по его идентификатору.
        
        :param price_id: Параметр Price_id — это уникальный идентификатор ценового диапазона, который вы
        хотите удалить из базы данных
        :return: логическое значение True.
        """
        self.cur.execute("DELETE FROM prices WHERE id=%s", (price_id,))
        self.conn.commit()
        logger.info('Диапазон цен удален из базы данных')
        return True

    def get_price_ranges_by_price(self, price):
        """
        Функция извлекает диапазоны цен из базы данных на основе заданной цены.
        
        :param price: Параметр «цена» — это значение, которое вы хотите использовать для фильтрации
        диапазонов цен. Запрос извлекает все диапазоны цен, в которых данная цена попадает между
        столбцами «ot» и «ido» в таблице «цены»
        :return: Цена варьируется от базы данных, которая включает данную цену.
        """
        self.cur.execute("SELECT * FROM prices WHERE %s BETWEEN ot AND ido", (price,))
        logger.info('Диапазоны цен получены из базы данных')
        return self.cur.fetchall()
    
    def check_prices_exists(self, id):
        """
        Функция проверяет, существует ли в базе данных диапазон цен для данного идентификатора.
        
        :param id: Параметр «id» — это идентификатор ценового диапазона, наличие которого вы хотите
        проверить в базе данных
        :return: логическое значение, указывающее, существует ли в базе данных ценовой диапазон с данным
        идентификатором.
        """
        try:
            self.cur.execute("SELECT * FROM prices WHERE id = %s", (id,))
            logger.info('Проверка наличия диапазона цен в базе данных')
        except Exception as e:
            logger.error(f"Ошибка при работе с базой данных: {e}")
            return False
        result = self.cur.fetchone()
        return bool(result)
