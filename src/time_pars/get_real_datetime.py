#/src/time/get_real_datetime.py
from datetime import datetime, timedelta
from logging import getLogger
from log_scripts.set_logger import set_logger
# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def get_real_datetime(relative_time : str):
    # Проверяем, если значение "Вчера"
    if "Вчера" in relative_time:
        # Получаем время из строки
        time_str = relative_time.split(" в ")[1]
        # Преобразуем время в объект datetime.time
        time = datetime.strptime(time_str, "%H:%M").time()
        # Получаем текущую дату и вычитаем один день
        today = datetime.now().date() - timedelta(days=1)
        # Объединяем дату и время в объект datetime
        dt = datetime.combine(today, time)
        return dt.strftime('%d.%m.%Y %H:%M'), int(dt.timestamp())
    else:
        delta = timedelta(seconds=0)
        month = "00"
        # Получаем количество минут/часов, которое нужно вычесть
        if "секунд" in relative_time:
            delta = timedelta(seconds=int(relative_time.split()[0]))
        elif "минут" in relative_time:
            delta = timedelta(minutes=int(relative_time.split()[0]))
        elif "час" in relative_time:
            delta = timedelta(hours=int(relative_time.split()[0]))
        elif "день" in relative_time:
            delta = timedelta(days=int(relative_time.split()[0]))
        
       
        # Проверяем, если месяц указан текстом
        elif 'января' in relative_time:
            month = '01'
        elif 'февраля' in relative_time:
            month = '02'
        elif 'марта' in relative_time:
            month = '03'
        elif 'апреля' in relative_time:
            month = '04'
        elif 'мая' in relative_time:
            month = '05'
        elif 'июня' in relative_time:
            month = '06'
        elif 'июля' in relative_time:
            month = '07'
        elif 'августа' in relative_time:
            month = '08'
        elif 'сентября' in relative_time:
            month = '09'
        elif 'октября' in relative_time:
            month = '10'
        elif 'ноября' in relative_time:
            month = '11'
        elif 'декабря' in relative_time:
            month = '12'
        else:
            # Если значение неизвестно, возвращаем None
            return datetime.now().strftime('%d.%m.%Y %H:%M') , int(datetime.now().timestamp())
        # Вычитаем значение из текущего момента времени
        if month == "00":
            dt = datetime.now() - delta
        else:
            # Получаем день из строки
            day = int(relative_time.split()[0])
            year = datetime.now().year
            if datetime.now().month < int(month):
                year = datetime.now().year - 1
            # Получаем время из строки
            time_str = relative_time.split(" в ")[1]
            time = datetime.strptime(time_str, "%H:%M").time()
            dt = datetime(year, int(month), day, time.hour, time.minute)
        return dt.strftime('%d.%m.%Y %H:%M'), int(dt.timestamp())

def main():
    """print(get_real_datetime("1 секунду назад"))
    print(get_real_datetime("5 минут назад"))
    print(get_real_datetime("2 часа назад"))
    print(get_real_datetime("14 часов назад"))
    print(get_real_datetime("Вчера в 12:00"))
    print(get_real_datetime("1 января в 12:00"))
    print(get_real_datetime("1 февраля в 12:00"))
    print(get_real_datetime("18 февраля в 13:28"))
    print(get_real_datetime("3 марта в 12:00"))
    print(get_real_datetime("13 апреля в 12:00"))
    print(get_real_datetime("1 мая в 12:00"))
    print(get_real_datetime("1 июля в 12:00"))
    print(get_real_datetime("12 августа в 12:00"))
    print(get_real_datetime("1 сентября в 12:00"))
    print(get_real_datetime("11 октября в 12:00"))
    print(get_real_datetime("1 ноября в 12:00"))
    print(get_real_datetime("1 декабря в 12:00"))"""

if __name__ == "__main__":
    main()