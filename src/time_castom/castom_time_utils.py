from datetime import datetime, time, timedelta
from random import randint
from time import sleep
from configuration.read_strings_from_file import read_strings_from_file

active_periods = [
        (time(8, 0), time(10, 15)),
        (time(13, 0), time(15, 15)),
        (time(16, 15), time(18, 30)),
        (time(21, 45), time(23, 59)),
        (time(0, 0), time(0, 15))
    ]

strings_dict = read_strings_from_file()
time_for_otklik = int(strings_dict["time_for_otklik"])

active_sleep_time_min = time_for_otklik - 10
active_sleep_time_max = time_for_otklik + 10

inactive_sleep_time_min = int(strings_dict["inactive_sleep_time_min"])
inactive_sleep_time_max = int(strings_dict["inactive_sleep_time_max"])

def get_next_active_period_start():
    now = datetime.now().time()
    
    for start, _ in active_periods:
        if now < start:
            return start
    return active_periods[0][0]  # Возвращаем начало первого активного периода следующего дня

def is_active_time():
    now = datetime.now().time()

    for start, end in active_periods:
        if start <= now <= end:
            return True
    return False

def get_sleep_time():
    if is_active_time():
        # В активный период функция возвращает случайное число от 5 до 10 секунд
        return randint(active_sleep_time_min, active_sleep_time_max)
    else:
        next_active_start = get_next_active_period_start()
        now = datetime.now().time()
        # Вычисляем время до следующего активного периода
        time_to_next_active = timedelta(hours=next_active_start.hour, minutes=next_active_start.minute) - timedelta(hours=now.hour, minutes=now.minute)
        time_to_next_active_seconds = max(0, time_to_next_active.total_seconds())
        
        # Осталось 30 минут или меньше до начала активного периода
        if time_to_next_active_seconds <= inactive_sleep_time_min:
            return time_to_next_active_seconds + randint(active_sleep_time_min, active_sleep_time_max)
        
        # Осталось больше 30 минут, но меньше 45 минут до начала активного периода
        if inactive_sleep_time_min < time_to_next_active_seconds < inactive_sleep_time_max:
            return randint(inactive_sleep_time_min, int(time_to_next_active_seconds))
        
        # Осталось 45 минут или больше до начала активного периода
        return randint(inactive_sleep_time_min, inactive_sleep_time_max)

# def get_sleep_time():
#     if is_active_time():
#         return randint(5, 10)  # Случайное время сна в активные периоды (5-10 секунд)
#     else:
#         next_active_start = get_next_active_period_start()
#         now = datetime.now().time()
#         time_to_next_active = timedelta(hours=next_active_start.hour, minutes=next_active_start.minute) - timedelta(hours=now.hour, minutes=now.minute)
#         time_to_next_active_seconds = max(0, time_to_next_active.total_seconds())
#         #return min(1800 + randint(-900, 900), time_to_next_active_seconds + 1)  # Возвращаем либо случайное время до 45 минут, либо время до начала следующего активного периода
#         return min(1800, time_to_next_active_seconds) if time_to_next_active_seconds >= 1800 else randint(0, int(time_to_next_active_seconds))

# while True:
#     # Ваш код...
#     sleep_time = get_sleep_time()
#     sleep(sleep_time)
