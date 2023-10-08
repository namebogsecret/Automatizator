import sqlite3

from src.database.login_to_sql_server import login_to_sql_server
from src.constants.pathes import db_path
from src.parsing_card.pars_prices import parse_prices
from src.database.price_database import PricesDatabase




# Открываем соединение с базой данных
conn = login_to_sql_server()

if conn is None:
    exit()
# Создаем курсор для выполнения запросов
cur = conn.cursor()

# Выполняем запрос, получаем результаты
cur.execute("SELECT ot_do, price, id FROM Applications")
results = cur.fetchall()

# Закрываем соединение
pd = PricesDatabase(conn)
# Открываем файл для записи
with open('prices_parsed5.txt', 'w') as f:
    # Проходим по результатам и записываем их построчно в файл
    for row in results:
        lower, upper = parse_prices(row[0], row[1])
        pd.add_price_range( row[2], lower, upper)
        """if row[1] != "":
            f.write(f"{lower},\t{upper},\t{row[0]},\t\t{row[1]}\n")"""
cur.close()
conn.close()
