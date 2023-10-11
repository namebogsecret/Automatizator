"""
Модуль для обработки статистики
"""

from datetime import datetime
from time import sleep
from os.path import exists
import pandas as pd
import threading
import pickle



from src.ssh.sshtunnel_creater import SshTunnelCreator
from src.database.ssh_login import SshDbConnector
from src.parsing_card.pars_prices import parse_prices
from src.plots.plot_data_week_month import plot_data_week_month
from src.plots.plot_data_hour_week import plot_data_day_hour

if exists('data.pkl'):
    with open('data.pkl', 'rb') as f:
        df = pickle.load(f)
else:
    QUERY = """
            SET datestyle TO 'European,SQL';
            SELECT 
                "datetime",
                EXTRACT(DOW FROM "datetime"::timestamp) AS day_of_week,
                EXTRACT(MONTH FROM "datetime"::timestamp) AS month,
                EXTRACT(HOUR FROM "datetime"::timestamp) AS hour,
                price,
                ot_do,
                id,
                subject,
                address,
                class_description,
                school,
                modified,
                timestamp_last,
                schedule,
                distant,
                name,
                posted,
                CASE WHEN img1 IS NOT NULL THEN TRUE ELSE FALSE END AS has_img1,
                CASE WHEN img2 IS NOT NULL THEN TRUE ELSE FALSE END AS has_img2
            FROM applications;
            """
    # После создания туннеля и подключения к базе данных:

    """day_query = 
    SELECT 
        TO_CHAR(TO_TIMESTAMP('16.08.2023', 'DD.MM.YYYY'), 'Day') AS day_name,
        EXTRACT(DOW FROM TO_TIMESTAMP('16.08.2023', 'DD.MM.YYYY')) AS day_number;
    """




    TUNNEL = SshTunnelCreator()
    tunnel_thread = threading.Thread(target=TUNNEL.create_tunnel)
    tunnel_thread.start()

    while not TUNNEL.tonnel_created:
        sleep(0.1)
        continue

    local_port = TUNNEL.local_port
    connect = SshDbConnector(local_port).db_connect()

    while not connect:
        sleep(0.1)
        continue
    """result_df = pd.read_sql(day_query, connect)
    print(result_df)
    exit()"""
    df = pd.read_sql(QUERY, connect)
    # Сериализация и сохранение данных
    with open('data.pkl', 'wb') as f:
        pickle.dump(df, f)

# Предположим, что данные загружены в DataFrame с именем df
df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M'))
df['price_ot'], df['price_do'] = zip(*df.apply(lambda row: parse_prices(row['ot_do'], row['price']), axis=1))


# Например, для диапазона цен от 0 до 1000
price_range = (2500, 10000)
filtered_df = df[(df['price_ot'] >= price_range[0]) & (df['price_do'] <= price_range[1])]

#plot_data_week_month(filtered_df, f"Заявки для диапазона цен: {price_range}")
# вызываем функцию для построения графика
plot_data_day_hour(filtered_df, "Заявки по часам и дням недели", 1)