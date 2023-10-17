from time import sleep, time
from datetime import datetime, timedelta
from sys import exit as sys_exit
from telegram_bot.telegram_send_note import TelegramBots
from logging import getLogger
from log_scripts.set_logger import set_logger
from constants.flags import flag
from constants.time_container import time_container

logger = getLogger(__name__)
logger = set_logger(logger)


#@profile
def timer():
    global time_container
    global flag
    bots3 = TelegramBots(3)
    sleep(30)
    times = 0
    while not flag.stop:
        times += 1
        sleep(10)
        time_passed = datetime.now() - time_container.start_time
        #logger.info("Прошло %s секунд с момента запуска программы",
        # time_passed.seconds)
        #app.time_from_start["text"] = str(strftime( "%H:%M:%S",
        # gmtime(time_passed.seconds)))

        if times >= 6:
            try:
                # Вычисляем разницу во времени
                time_from_otklik = time() - time_container.last_time_otklik
                time_delta = timedelta(seconds=time_from_otklik)
                formatted_time = str(time_delta).split('.')[0]
                bots3.to_developer(f"С обновления прошло: {formatted_time}")
                logger.info(f"С обновления прошло: {formatted_time}")
                if time_from_otklik > 60 * 10: #10 минут
                    logger.error(f"Слишком долго не обновлялись карточки {formatted_time}")
                    bots3.rassilka(f"Слишком долго не обновлялись карточки  {formatted_time}, возможно требуется внимание", False)
                    if time_from_otklik > 60 * 15: # 
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