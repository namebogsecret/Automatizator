#main.py
"""import sys
from os.path import dirname, abspath

if getattr(sys, 'frozen', False):
    src_path = sys._MEIPASS
else:
    src_path = dirname(abspath(__file__))
sys.path.append(src_path)"""
from src.configuration.read_strings_from_file import read_strings_from_file

from sys import exit as sys_exit
from datetime import datetime, timedelta
from random import randint
from threading import Thread
#import AppKit as appkit
from time import sleep, time #strftime, gmtime, 
from src.database.login_to_sql_server import login_to_sql_server
from src.constants.pathes import db_path
from src.otklik.last_cards_chek import last_cards_check
from src.parsing_cards.update_all_cards import CardUpdater
from logging import getLogger
from src.log_scripts.set_logger import set_logger
from src.log_scripts.set_logger import logs_dir, archive_large_logs, archive_old_logs
from src.webdriver.prepare_page import prepare_page
#from constants.pathes import stop_file
from src.webdriver.scroll import scroll_down
from gc import collect

#from tkinter import Tk
#from visual.form import App
#from constants.pathes import stop_file
from src.log_scripts.close_logs import close_log_files


#from visual.form import App

from src.constants.flags import flag
#import telegram_bot.telegram_bot_get_id as bot
from src.telegram_bot.telegram_send_note import TelegramBots
from src.otklik.is_it_on_the_page import WebScraper
#from constants.dict import dict_otklik
from src.sound.pik import pik
#from constants.dicts_def import dicts
#from utils.how_many_files import how_many_files
from src.configuration.read_dictionaries_from_file import read_dictionaries_from_file
import json

from src.stata.get_ostalos import get_ostalos
#from memory_profiler import profile

logger = getLogger(__name__)
logger = set_logger(logger)
last_time_otklik = time()
read_dictionaries_from_file('src/configuration/dictionaries_old.json')
strings_dict = read_strings_from_file()
cards_at_a_time = int(strings_dict["cards_at_a_time"])
time_for_otklik = int(strings_dict["time_for_otklik"])
scrolls = int(strings_dict["scrolls"])
url2 = strings_dict["second_url"]

form_width = 225
form_height = 345
start_time = datetime.now()
logger.info("Запуск программы в %s", start_time)
#cards_at_a_time = 20
#scrolls = 2

poluchat_li_ostalos = int(strings_dict["poluchat_li_ostalos"])


CAPTCHA_IS_SOLVED = False
#@profile
def timer():
    global CAPTCHA_IS_SOLVED
    global time_for_otklik
    strings_dict = read_strings_from_file()
    time_for_otklik = int(strings_dict["time_for_otklik"])
    bots3 = TelegramBots(3)
    sleep(30)
    times = 0
    while not flag.stop:
        times += 1
        sleep(10)
        time_passed = datetime.now() - start_time
        #logger.info("Прошло %s секунд с момента запуска программы",
        # time_passed.seconds)
        #app.time_from_start["text"] = str(strftime( "%H:%M:%S",
        # gmtime(time_passed.seconds)))

        if times >= 6 and CAPTCHA_IS_SOLVED == True:
            try:
                # Вычисляем разницу во времени
                time_from_otklik = time() - last_time_otklik
                time_delta = timedelta(seconds=time_from_otklik)
                formatted_time = str(time_delta).split('.')[0]
                bots3.to_developer(f"С обновления прошло: {formatted_time}")
                logger.info(f"С обновления прошло: {formatted_time}")
                if time_from_otklik > time_for_otklik * 3: #10 минут
                    logger.error(f"Слишком долго не обновлялись карточки {formatted_time}")
                    bots3.rassilka(f"Слишком долго не обновлялись карточки  {formatted_time}, возможно требуется внимание", False)
                    if time_from_otklik > time_for_otklik * 5: # 
                        logger.error(f"Слишком долго не обновлялись карточки {formatted_time} - Перезапуск")
                        bots3.rassilka(f"Слишком долго не обновлялись карточки  {formatted_time} - Перезапуск", False)
                        sys_exit("Error: too long not updating, trying to restart the bot")
                del time_from_otklik, formatted_time, time_delta
                times = 0
            except Exception as e:
                logger.error(e)
                logger.error("Не удалось отправить сообщение в телеграмм")
                times = 0
        del time_passed
#@profile
def main_loop():
    global last_time_otklik
    global scrolls
    global time_for_otklik
    global cards_at_a_time
    bots1 = TelegramBots(1)
    bots2 = TelegramBots(2)
    bots1.to_all_mine("Запустился бот %s" % start_time.strftime("%d.%m.%Y %H:%M:%S"),
                      False)

    sleep(30+randint(-10, 10))
    logger.info("Запуск главного цикла")
    #app.state_label["text"] = "State: Preparing page..."
    driver, x_coordinata = prepare_page(scrolls)
    #root.geometry(f"+{int(x_coordinata)}+{int(0)}")
    #Сделать перелогинивание!!!!!
    ciklov = 0
    #print(stop_file)
    #print(exists(stop_file))
    #while exists(stop_file):
    otklikov = 0
    vakansiy = 0
    deleted = 0
    errors = 0
    nepodhodit = 0
    banned = 0
    limited = 0

    some_errors = 0
    is_it_critical = 0
    global dicts
    ostalos_otklikov = 50

    if poluchat_li_ostalos == 1:
        try:

            if 0 <= datetime.now().minute <= 5:
                ostalos = get_ostalos(driver)
                sleep(20+randint(-5, 5))
                if not ostalos:
                    logger.error("Не удалось получить осталось")
                else:
                    ostalos_otklikov = ostalos
        except Exception as e:
            logger.error(f"Ошибка получения осталось: {e}")
    while not flag.stop:
        timer_start = time()
        archive_old_logs(logs_dir)
        archive_large_logs(logs_dir)
        if read_dictionaries_from_file('src/configuration/dictionaries_old.json'):
            logger.info("Словари обновлены")
        else:
            logger.error("Не удалось обновить словари")
        ciklov += 1
        logger.info("-----начался цикл %s ------", ciklov)
        #app.state_label["text"] = "State: Opening sql..."
        sql = login_to_sql_server(db_path)
        if sql is None:
            logger.error("Не удалось подключиться к базе данных")
            return None
        
        cardupdater = CardUpdater(driver,sql )
        #app.state_label["text"] = "State: trying to work with cards..."
        delta = 0
        delta_otkl = 0
        #sleep(0.2)
        try:
            #app.state_label["text"] = "State: Updating cards..."
            cards_parsed = cardupdater.update_all_cards()
            logger.info("Карточки обновлены")
            #lookup_deleted(cards_parsed,sql)
            if cards_parsed != []:
                #app.state_label["text"] = "State: Checking last cards..."
                logger.info("Проверка последних карточек")
                o1, v1, d1, e1, n1, b1, l1 = last_cards_check(cards_at_a_time, sql,
                                                              driver, cards_parsed,
                                                              otklikov, vakansiy,
                                                              deleted, errors,
                                                              nepodhodit, banned,
                                                              limited)
                logger.info("Последние карточки проверены")
                delta = max (o1 - otklikov, v1 - vakansiy, d1 - deleted,
                             e1 - errors, n1 - nepodhodit, b1 - banned, l1 - limited)
                delta_otkl = o1 - otklikov
                otklikov, vakansiy, deleted, errors, nepodhodit, banned, limited = o1, v1, d1, e1, n1, b1, l1
                """app.sent_number["text"] = str(otklikov)
                app.vakansii_number["text"] = str(vakansiy)
                app.delete_number["text"] = str(deleted)
                app.error_number["text"] = str(errors)
                app.nepodhodit_number["text"] = str(nepodhodit)
                app.banned_number["text"] = str(banned)
                app.limited_number["text"] = str(limited)"""

                if poluchat_li_ostalos == 1:
                    #если сейчас время от 0 до 5 минут каждый час, то отправляем статистику
                    try:
                        if 0 <= datetime.now().minute <= 5:
                            ostalos = get_ostalos(driver)
                            sleep(10)
                            if not ostalos:
                                logger.error("Не удалось получить осталось")
                            else:
                                ostalos_otklikov = ostalos
                    except Exception as e:
                        logger.error(f"Ошибка получения осталось: {e}")
                
                bots2.to_developer(f"""Цикл: {str(ciklov)} \nОткликов: {str(otklikov)} \nВакансий: {str(vakansiy)} \nУдаленных: {str(deleted)} \nОшибок: {str(errors)}  \nНеподходящих: {str(nepodhodit)} \nЗабаненных: {str(banned)} \nЛимитов: {str(limited)} \nВремя: {str(datetime.now().strftime('%H:%M:%S'))}\nОсталось: {str(ostalos_otklikov)}""")
                last_time_otklik = time()
            else:
                logger.error("Нет новых карточек none ")
                some_errors += 1
                driver.close()
                driver, x_coordinata = prepare_page(0) 
                
        except Exception as e:
            logger.error(e)
            some_errors += 1
            #app.state_label["text"] = "State: Error while working with cards..."
            logger.error("Не удалось обновить карточки")
        if some_errors > 5:
            logger.error("Слишком много ошибок")
            bots1.rassilka("""Больше 5 ошибок, возможно требуется внимание""")
            some_errors = 0
            is_it_critical += 1
            if is_it_critical > 5:
                logger.error("Слишком много критических ошибок")
                bots1.rassilka("""3 критических ошибки, пробуем перезапустить бота""")
                # Завершение программы
                sys_exit("Error: too many critical errors, trying to restart the bot")

        logger.info(f"-----идет цикл {ciklov} ------")
        timer_stop = time()
        #driver.save_screenshot(f"screenshot_{timer_stop}.png")
        strings_dict = read_strings_from_file()
        cards_at_a_time = int(strings_dict["cards_at_a_time"])
        time_for_otklik = int(strings_dict["time_for_otklik"])
        proshlo_vremeni = timer_stop - timer_start
        if not flag.stop and delta > 0 and delta_otkl == 0 and proshlo_vremeni < time_for_otklik:
            try:
                driver.get(url2)
                strings_dict = read_strings_from_file()
                scrolls = int(strings_dict["scrolls"])
                scroll_down(driver, scrolls)
                #app.state_label["text"] = "State: Main page opening..."
                sleep(60 + randint(-20, 20))
                cardupdater = CardUpdater(driver,sql )
                cardupdater.update_all_cards()
                ws = WebScraper(driver, "dict_otklik")
                new_messages = ws.is_it_on_the_page("new_messages")
                if new_messages:
                    number_of_messages = new_messages.text
                    #app.state_label["text"] = f"Have new messages:
                    # {number_of_messages}"
                    bots1.rassilka(f"Новые сообщения: {number_of_messages}", False)
                    logger.info(f"Have new messages: {number_of_messages}")
                    """for tri_pika in range(3):
                        pik(4000)
                        sleep(0.5)"""
            except Exception as e:
                logger.error(e)
                logger.error("Не удалось перейти на страницу https://repetitors.info/backoffice/n.php")
                
        #app.state_label["text"] = "State: closing sql..."
        if delta_otkl > 0:
            flag.update_now = True
        # обновляем значение числа на метке
        sql.close()
        #app.loops_number["text"] = str(ciklov)
        time_to_sleep = time_for_otklik + randint(-30, 30)
        #time_of_continue = datetime.now() + timedelta(seconds=time_to_sleep)
        #app.state_label["text"] = "State: will continue in "
        # + str(time_of_continue.strftime("%H:%M:%S")) + " seconds"
        random_time = randint(0, 120)
        for cikl_time in range(time_to_sleep):
            second_timer_stop = time()
            proshlo_vremeni = second_timer_stop - timer_start
            if flag.stop or flag.update_now or proshlo_vremeni > time_for_otklik + random_time:
                break
            sleep(2+randint(-1, 1))
        
        pause_counter = 0
        while flag.pause and not flag.update_now:
            
            pause_counter += 1
            #app.state_label["text"] = "State: Paused for {pause_counter} seconds"
            sleep(2 + randint(-1, 1))
        #app.state_label["text"] = "State: Trying to open main page."
        collect()
        if not flag.stop:
            strings_dict = read_strings_from_file()
            cards_at_a_time = int(strings_dict["cards_at_a_time"])
            time_for_otklik = int(strings_dict["time_for_otklik"])
            try:
                driver.get(url2)
                strings_dict = read_strings_from_file()
                scrolls = int(strings_dict["scrolls"])
                scroll_down(driver, scrolls)
                #app.state_label["text"] = "State: Main page opening..."
                sleep(20 + randint(-3, 3))
                scroll_down(driver, 2)
                ws = WebScraper(driver, "dict_otklik")
                new_messages = ws.is_it_on_the_page("new_messages")
                if new_messages:
                    number_of_messages = new_messages.text
                    #app.state_label["text"] = f"Have new messages:
                    # {number_of_messages}"
                    bots1.rassilka(f"Новые сообщения: {number_of_messages}", False)
                    logger.info(f"Have new messages: {number_of_messages}")
                    for tri_pika in range(3):
                        pik(3000)
                else:
                    #app.state_label["text"] = "State: No new messages"
                    logger.info("No new messages")
                sleep(2 + randint(-1, 1))
            except Exception as e:
                logger.error(e)
                logger.error("Не удалось перейти на страницу https://repetitors.info/backoffice/n.php")
                logger.info("Закрытие и сохранение соединения с базой данных")
                #app.state_label["text"] =
                # "State: Error while opening main page, reloading..."
                sleep(10 + randint(-2, 2))
                continue
        logger.info("Закрытие и сохранение соединения с базой данных")
        #how_many_files()
                # Save cookies to a file
        logger.info("Сохранение cookies в файл")
        try:
            with open('cookies.txt', 'w') as file:
                json.dump(driver.get_cookies(), file)
        except Exception as e:
            logger.error(e)
            logger.error("Не удалось сохранить cookies в файл")
        logger.info("-----закончился цикл %s ------", ciklov)
        flag.update_now = False
    # Закрытие экземпляра драйвера
    
    #app.state_label["text"] = "State: Closing driver..."
    driver.close()
    bots1.to_all_mine("Бот выключается %s" % start_time.strftime("%d.%m.%Y %H:%M:%S"),
                      False)


timer_thread = Thread(target=timer)
timer_thread.start()

"""telegram_bot_thread = Thread(target=bot.my_telegram_bot)
telegram_bot_thread.start()"""
# создаем объект главного потока
main_thread = Thread(target=main_loop)
# устанавливаем флаг, чтобы поток мог проверять его периодически



# запускаем главный поток
main_thread.start()

#root = Tk()

#root.title("Автоотклики")
#root.geometry(f"{form_width}x{form_height}")
"""# Получение списка экранов
screens = appkit.NSScreen.screens()

# Проверка наличия второго экрана
if len(screens) > 1:
    # Получение размеров экранов
    screen_width_1 = screens[0].frame().size.width
    screen_height_1 = screens[0].frame().size.height
    screen_width_2 = screens[1].frame().size.width
    screen_height_2 = screens[1].frame().size.height

    # Вычисление координат x и y окна
    x = screen_width_1 + screen_height_2/2
    y = 0

    # Установка координат x и y окна
    root.geometry(f"+{int(x)}+{int(y)}")"""
#root.resizable(False, False)
#app = App(master=root, main_thread=main_thread)
#app.mainloop()
#logger.info("Завершение работы графического интерфейса")
main_thread.join()
logger.info("Завершение работы программы")


try:
    sys_exit("Error: exiting the program")
    close_log_files()
    #root.destroy()
except Exception as e:
    logger.info(f"Завершение жестко {e}")
#logger.info("Завершение работы программы2")
