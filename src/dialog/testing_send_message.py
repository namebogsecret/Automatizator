from otklik.is_it_on_the_page import WebScraper
from log_scripts.set_logger import set_logger
from logging import getLogger

from selenium.webdriver.common.keys import Keys

from time import sleep

logger = getLogger(__name__)
logger = set_logger(logger)

def testing_send_message(driver, text) -> str:


    w1 = WebScraper(driver, "dict_otklik")
    # Find element by class ending with 'faTkYO'
    if not w1.is_it_on_the_page("chat_page"):
        logger.info("Нет чата")
        return None
    #print(text)
    text_area = w1.is_it_on_the_page("chat_textarea")
    if not text_area:
        logger.info("Нет поля для ввода сообщения")
        return None
    text_area.send_keys(text)
    logger.info("Заполнил сообщение")
    sleep(1)
    #send_button = w1.is_it_on_the_page("chat_send_button")
    """if not send_button:
        logger.info("Нет кнопки отправки сообщения")
        return "No send button"""
    text_area.send_keys(Keys.RETURN)
    #send_button.click()
    logger.info("Отправил сообщение")
    sleep(1)
    return "OK"
        

