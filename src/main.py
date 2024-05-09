#main.py
"""import sys
from os.path import dirname, abspath

if getattr(sys, 'frozen', False):
    src_path = sys._MEIPASS
else:
    src_path = dirname(abspath(__file__))
sys.path.append(src_path)"""
import sys
from configuration.read_strings_from_file import read_strings_from_file

from sys import exit as sys_exit
from datetime import datetime, timedelta
from random import randint
from threading import Thread
#import AppKit as appkit
from time import sleep, time #strftime, gmtime, 
from database.login_to_sql_server import login_to_sql_server
from constants.pathes import db_path
from otklik.last_cards_chek import last_cards_check
from parsing_cards.update_all_cards import CardUpdater
from logging import getLogger
import log_scripts.set_logger
from log_scripts.set_logger import set_logger
from log_scripts.set_logger import logs_dir, archive_large_logs, archive_old_logs
from webdriver.prepare_page import prepare_page
#from constants.pathes import stop_file
from webdriver.scroll import scroll_down
from gc import collect

#from tkinter import Tk
#from visual.form import App
#from constants.pathes import stop_file
from log_scripts.close_logs import close_log_files


#from visual.form import App

from constants.flags import flag
#import telegram_bot.telegram_bot_get_id as bot
from telegram_bot.telegram_send_note import TelegramBots
from otklik.is_it_on_the_page import WebScraper
#from constants.dict import dict_otklik
from sound.pik import pik
#from constants.dicts_def import dicts
#from utils.how_many_files import how_many_files
from configuration.read_dictionaries_from_file import read_dictionaries_from_file
import json
import os
from stata.get_ostalos import get_ostalos
#from memory_profiler import profile
from utils.web_hook import WebhookSender

from time_castom.castom_time_utils import get_sleep_time


first_time_timout = 1 # 0 - не ждать при первом запуске, 1 - ждать

def set_affinity(cores):
    """ Устанавливает аффинность (привязку) процесса к определенным ядрам. """
    pid = os.getpid()
    os.sched_setaffinity(pid, cores)
set_affinity([1])

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

with open ("last_update.txt", "w") as file:
    file.write(str(datetime.now()))
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
                #logger.info(f"С обновления прошло: {formatted_time}")
                if time_from_otklik > time_for_otklik * 5: #10 минут
                    #logger.error(f"Слишком долго не обновлялись карточки {formatted_time}")
                    bots3.rassilka(f"Слишком долго не обновлялись карточки  {formatted_time}, возможно требуется внимание", False)
                    if time_from_otklik > time_for_otklik * 7: # 
                        #logger.error(f"Слишком долго не обновлялись карточки {formatted_time} - Перезапуск")
                        bots3.rassilka(f"Слишком долго не обновлялись карточки  {formatted_time} - Перезапуск", False)
                        sys_exit("Error: too long not updating, trying to restart the bot")
                del time_from_otklik, formatted_time, time_delta
                times = 0
            except Exception as e:
                #logger.error(e)
                #logger.error("Не удалось отправить сообщение в телеграмм")
                times = 0
        del time_passed
#@profile

class driver_manager():
    def __init__(self, scrolls):
        self._set_driver(scrolls)
        self.scrolls = scrolls
    
    def check(self):
        try:
            self.driver.title
            return True
        except:
            return False
    
    def get_driver(self, scrols = 0):
        if self.check():
            return self.driver
        else:
            return self._set_driver(scrols)

    def _set_driver(self, scrolls):
        try:
            self.driver, _ = prepare_page(scrolls)
        except Exception as e:
            logger.error(e)
            self.driver = None
        if self.check():
            return self.driver
        else:
            return None

    def reset(self,scrolls=0):
        self.delete()
        return self._set_driver(scrolls)
    
    def delete(self):
        try:
            self.driver.close()
        except Exception:
            pass
        self.driver = None

def main_loop():
    global last_time_otklik
    global scrolls
    global time_for_otklik
    global cards_at_a_time
    global first_time_timout
    bots1 = TelegramBots(1)
    bots2 = TelegramBots(2)
    bots1.to_all_mine("Запустился бот %s" % start_time.strftime("%d.%m.%Y %H:%M:%S"),
                      False)
    if first_time_timout == 0:
        first_time_timout = 1
        sleep_time = 0
        time_to_sleep = 20
    else:
        sleep_time = get_sleep_time()
        time_to_sleep = sleep_time + randint(-120, 120)
    logger.info("Время до первого запуска: %s", time_to_sleep)
    sleep(time_to_sleep + randint(-10, 10))
    logger.info("Запуск главного цикла")
    #app.state_label["text"] = "State: Preparing page..."
    my_driver_manager = driver_manager(scrolls)
    driver = my_driver_manager.get_driver()
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
                ostalos = get_ostalos(my_driver_manager.get_driver())
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
        sql = login_to_sql_server()
        if sql is None:
            logger.error("Не удалось подключиться к базе данных")
            return None
        
        cardupdater = CardUpdater(my_driver_manager.get_driver(),sql )
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
                                                              my_driver_manager.get_driver(), cards_parsed,
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
                            ostalos = get_ostalos(my_driver_manager.get_driver())
                            sleep(10 + randint(-3, 3))
                            if not ostalos:
                                logger.error("Не удалось получить осталось")
                            else:
                                ostalos_otklikov = ostalos
                    except Exception as e:
                        logger.error(f"Ошибка получения осталось: {e}")
                sleep_time = get_sleep_time()
                time_to_sleep = max (0, int(sleep_time) + randint(-120, 120))
                bots2.to_developer(f"""Цикл: {str(ciklov)} \nОткликов: {str(otklikov)} \nВакансий: {str(vakansiy)} \nУдаленных: {str(deleted)} \nОшибок: {str(errors)}  \nНеподходящих: {str(nepodhodit)} \nЗабаненных: {str(banned)} \nЛимитов: {str(limited)} \nВремя: {str(datetime.now().strftime('%H:%M:%S'))}\nОсталось: {str(ostalos_otklikov)}\nСпать: {str(time_to_sleep)}""")
                with open ("last_update.txt", "w") as file:
                    file.write(str(datetime.now()))
                last_time_otklik = time()
            else:
                logger.error("Нет новых карточек none ")
                some_errors += 1
                my_driver_manager.reset()
                
        except Exception as e:
            sleep_time = get_sleep_time()
            time_to_sleep = max (0, int(sleep_time) + randint(-120, 120))
            logger.error(e)
            some_errors += 1
            #app.state_label["text"] = "State: Error while working with cards..."
            sender = WebhookSender()
            data = {
                'service': 'otklik',
                'event': 'error',
                'error': True,
                'message': f"Ошибка при обновлении карточек {e}"
            }
            response = sender.send_webhook(data)
            logger.error("Не удалось обновить карточки")
            my_driver_manager.reset() 
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
                my_driver_manager.get_driver().get(url2)
                strings_dict = read_strings_from_file()
                scrolls = int(strings_dict["scrolls"])
                scroll_down(my_driver_manager.get_driver(), scrolls)
                #app.state_label["text"] = "State: Main page opening..."
                sleep(60 + randint(-20, 20))
                cardupdater = CardUpdater(my_driver_manager.get_driver(),sql )
                cardupdater.update_all_cards()
                ws = WebScraper(my_driver_manager.get_driver(), "dict_otklik")
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
        # if delta_otkl > 0:
        #     flag.update_now = True
        # обновляем значение числа на метке
        sql.close()
        #app.loops_number["text"] = str(ciklov)

        logger.info("Время до следующего запуска: %s", time_to_sleep)
        #time_of_continue = datetime.now() + timedelta(seconds=time_to_sleep)
        #app.state_label["text"] = "State: will continue in "
        # + str(time_of_continue.strftime("%H:%M:%S")) + " seconds"
        random_time = randint(0, 120)
        for cikl_time in range(time_to_sleep):
            second_timer_stop = time()
            proshlo_vremeni = second_timer_stop - timer_start
            if flag.stop or flag.update_now or proshlo_vremeni > time_to_sleep + random_time:
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
                my_driver_manager.get_driver().get(url2)
                strings_dict = read_strings_from_file()
                scrolls = int(strings_dict["scrolls"])
                scroll_down(my_driver_manager.get_driver(), scrolls)
                #app.state_label["text"] = "State: Main page opening..."
                sleep(20 + randint(-3, 3))
                #scroll_down(my_driver_manager.get_driver(), 2)
                ws = WebScraper(my_driver_manager.get_driver(), "dict_otklik")
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
                json.dump(my_driver_manager.get_driver().get_cookies(), file)
        except Exception as e:
            logger.error(e)
            logger.error("Не удалось сохранить cookies в файл")
        logger.info("-----закончился цикл %s ------", ciklov)
        flag.update_now = False

        
    # Закрытие экземпляра драйвера
    
    #app.state_label["text"] = "State: Closing driver..."
    my_driver_manager.delete()
    bots1.to_all_mine("Бот выключается %s" % start_time.strftime("%d.%m.%Y %H:%M:%S"),
                      False)



import signal

def signal_explanation(sig):
    """1) SIGHUP   2) SIGINT   3) SIGQUIT  4) SIGILL
    5) SIGTRAP  6) SIGABRT  7) SIGBUS   8) SIGFPE
    9) SIGKILL 10) SIGUSR1 11) SIGSEGV 12) SIGUSR2
    13) SIGPIPE 14) SIGALRM 15) SIGTERM 16) SIGSTKFLT
    17) SIGCHLD 18) SIGCONT 19) SIGSTOP 20) SIGTSTP
    21) SIGTTIN 22) SIGTTOU 23) SIGURG  24) SIGXCPU
    25) SIGXFSZ 26) SIGVTALRM   27) SIGPROF 28) SIGWINCH
    29) SIGIO   30) SIGPWR  31) SIGSYS  34) SIGRTMIN
    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3  38) SIGRTMIN+4
    39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
    43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12
    47) SIGRTMIN+13 48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14
    51) SIGRTMAX-13 52) SIGRTMAX-12 53) SIGRTMAX-11 54) SIGRTMAX-10
    55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7  58) SIGRTMAX-6
    59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
    63) SIGRTMAX-1  64) SIGRTMAX 65) SIGPOLL  66) SIGLOST 67) SIGXFSZ 68) SIGXCPU"""
    sig_num = {
        1: "SIGHUP",
        2: "SIGINT",
        3: "SIGQUIT",
        4: "SIGILL",
        5: "SIGTRAP",
        6: "SIGABRT",
        7: "SIGBUS",
        8: "SIGFPE",
        9: "SIGKILL",
       10: "SIGUSR1",
       11: "SIGSEGV",
       12: "SIGUSR2",
       13: "SIGPIPE",
       14: "SIGALRM",
       15: "SIGTERM",
       16: "SIGSTKFLT",
       17: "SIGCHLD",
       18: "SIGCONT",
       19: "SIGSTOP",
       20: "SIGTSTP",
       21: "SIGTTIN",
       22: "SIGTTOU",
       23: "SIGURG",
       24: "SIGXCPU",
       25: "SIGXFSZ",
       26: "SIGVTALRM",
       27: "SIGPROF",
       28: "SIGWINCH",
       29: "SIGIO",
       30: "SIGPWR",
       31: "SIGSYS",
       34: "SIGRTMIN",
       35: "SIGRTMIN+1",
       36: "SIGRTMIN+2",
       37: "SIGRTMIN+3",
       38: "SIGRTMIN+4",
       39: "SIGRTMIN+5",
       40: "SIGRTMIN+6",
       41: "SIGRTMIN+7",
       42: "SIGRTMIN+8",
       43: "SIGRTMIN+9",
       44: "SIGRTMIN+10",
       45: "SIGRTMIN+11",
       46: "SIGRTMIN+12",
       47: "SIGRTMIN+13",
       48: "SIGRTMIN+14",
       49: "SIGRTMIN+15",
       50: "SIGRTMAX-14",
       51: "SIGRTMAX-13",
       52: "SIGRTMAX-12",
       53: "SIGRTMAX-11",
       54: "SIGRTMAX-10",
       55: "SIGRTMAX-9",
       56: "SIGRTMAX-8",
       57: "SIGRTMAX-7",
       58: "SIGRTMAX-6",
       59: "SIGRTMAX-5",
       60: "SIGRTMAX-4",
       61: "SIGRTMAX-3",
       62: "SIGRTMAX-2",
       63: "SIGRTMAX-1",
       64: "SIGRTMAX",
       65: "SIGPOLL",
       66: "SIGLOST",
       67: "SIGXFSZ",
       68: "SIGXCPU"
}

    # sig_cases = {
    #     signal.SIGINT: "Keyboard interrupt",
    #     signal.SIGTERM: "Termination signal",
    #     signal.SIGABRT: "Abnormal termination",
    #     signal.SIGFPE: "Floating point exception",
    #     signal.SIGILL: "Illegal instruction",
    #     signal.SIGSEGV: "Segmentation fault",
    #     signal.SIGPIPE: "Broken pipe",
    #     signal.SIGALRM: "Alarm clock",
    #     signal.SIGCHLD: "Child process terminated",
    #     signal.SIGCONT: "Continue executing, if stopped",
    #     signal.SIGTSTP: "Stop executing",
    #     signal.SIGTTIN: "Background process attempting read",
    #     signal.SIGTTOU: "Background process attempting write",
    #     signal.SIGUSR1: "User-defined signal 1",
    #     signal.SIGUSR2: "User-defined signal 2",
    #     signal.SIGPOLL: "Pollable event",
    #     signal.SIGPROF: "Profiling timer expired",
    #     signal.SIGSYS: "Bad system call",
    #     signal.SIGTRAP: "Trace/breakpoint trap",
    #     signal.SIGURG: "High bandwidth data is available at a socket",
    #     signal.SIGVTALRM: "Virtual timer expired",
    #     signal.SIGXCPU: "CPU time limit exceeded",
    #     signal.SIGXFSZ: "File size limit exceeded",
    #     signal.SIGWINCH: "Window size change",
    #     signal.SIGIO: "I/O now possible",
    #     signal.SIGPWR: "Power failure restart",
    #     signal.SIGINFO: "Status request from keyboard",
    #     signal.SIGLOST: "File lock lost",
    #     signal.SIGEMT: "EMT instruction",
    #     signal.SIGSTKFLT: "Stack fault on coprocessor",
    #     signal.SIGUNUSED: "Unused signal",
    #     signal.SIGBUS: "Bus error",
    #     signal.SIGKILL: "Kill signal",
    #     signal.SIGSTOP: "Stop signal",
    #     signal.SIGRTMIN: "Real-time signal",
    #     signal.SIGRTMAX: "Real-time signal"
    # }
    sig_cases = {
        1: "Hangup detected on controlling terminal or death of controlling process",
        2: "Interrupt from keyboard",
        3: "Quit from keyboard",
        4: "Illegal Instruction",
        5: "Trace/breakpoint trap",
        6: "Abort signal from abort(3)",
        7: "Bus error (bad memory access)",
        8: "Floating-point exception",
        9: "Kill signal",
        10: "User-defined signal 1",
        11: "Invalid memory reference",
        12: "User-defined signal 2",
        13: "Broken pipe: write to pipe with no readers",
        14: "Timer signal from alarm(2)",
        15: "Termination signal",
        16: "Stack fault on coprocessor (unused)",
        17: "Child stopped or terminated",
        18: "Continue if stopped",
        19: "Stop process",
        20: "Stop typed at terminal",
        21: "Terminal input for background process",
        22: "Terminal output for background process",
        23: "Urgent condition on socket (4.2BSD)",
        24: "CPU time limit exceeded (4.2BSD)",
        25: "File size limit exceeded (4.2BSD)",
        26: "Virtual alarm clock (4.2BSD)",
        27: "Profiling timer expired",
        28: "Window resize signal (4.3BSD, Sun)",
        29: "I/O now possible (4.2BSD)",
        30: "Power failure (System V)",
        31: "Bad system call",
        34: "Real-time signal 0",
        35: "Real-time signal 1",
        36: "Real-time signal 2",
        37: "Real-time signal 3",
        38: "Real-time signal 4",
        39: "Real-time signal 5",
        40: "Real-time signal 6",
        41: "Real-time signal 7",
        42: "Real-time signal 8",
        43: "Real-time signal 9",
        44: "Real-time signal 10",
        45: "Real-time signal 11",
        46: "Real-time signal 12",
        47: "Real-time signal 13",
        48: "Real-time signal 14",
        49: "Real-time signal 15",
        50: "Real-time signal 16",
        51: "Real-time signal 17",
        52: "Real-time signal 18",
        53: "Real-time signal 19",
        54: "Real-time signal 20",
        55: "Real-time signal 21",
        56: "Real-time signal 22",
        57: "Real-time signal 23",
        58: "Real-time signal 24",
        59: "Real-time signal 25",
        60: "Real-time signal 26",
        61: "Real-time signal 27",
        62: "Real-time signal 28",
        63: "Real-time signal 29",
        64: "Real-time signal 30",
        65: "Pollable event (Sys V). Synonym for SIGIO",
        66: "File lock lost (unused)",
        67: "File size limit exceeded",
        68: "CPU time limit exceeded"
    }

    return f"{sig_num[sig]} - {sig_cases[sig]}"

def signal_handler(sig, frame):
    logger.warning(f"Received signal: {sig} witch is {str(frame)} {signal_explanation(sig)}")
    try:
        sender = WebhookSender()
        data = {
            'service': 'otklik',
            'event': 'error',
            'error': True,
            'message': f"Received signal: {sig} witch is {str(frame)} {signal_explanation(sig)}"
        }
        response = sender.send_webhook(data)
        logger.warning("Удалось отправить сообщение в телеграмм")
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение в телеграмм: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

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
    sys.exit(0)
    sys_exit("Error: exiting the program")
    close_log_files()
    #root.destroy()
except Exception as e:
    logger.info(f"Завершение жестко {e}")
    sys.exit(0)
#logger.info("Завершение работы программы2")
