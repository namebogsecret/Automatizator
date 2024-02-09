from otklik.is_it_on_the_page import WebScraper
from log_scripts.set_logger import set_logger
from logging import getLogger

from selenium.webdriver.common.keys import Keys
from random import randint

from time import sleep
import re

logger = getLogger(__name__)
logger = set_logger(logger)

def send_text_with_shift_enter_short(text_area, text):

    # Разделение текста на части по символам перевода строки
    parts = text.split('\n')

    for part in parts[:-1]:  # Для всех частей, кроме последней
        text_area.send_keys(part)  # Отправка части текста
        text_area.send_keys(Keys.SHIFT, Keys.ENTER)  # Нажатие Shift+Enter

    text_area.send_keys(parts[-1])  # Отправка последней части текста
    logger.info("Заполнил сообщение")
    sleep(1)
    text_area.send_keys(Keys.ENTER)  # Нажатие Enter

def send_text_with_shift_enter(text_area, text, max_length=900):
    """
    Отправляет текст, разбивая его на сообщения длиной примерно 800-900 символов,
    разделяя по точкам или переводам строк.

    :param text_area: Элемент WebDriver, куда отправляется текст.
    :param text: Текст для отправки.
    :param logger: Логгер для записи действий.
    :param max_length: Максимальная длина одного сообщения.
    """
    max_length = max_length - randint(0, 100)  # Добавляем случайное значение до 100 символов
    # Разбиваем текст на предложения или блоки по точкам и переводам строк
    sentences = re.split(r'(?<=\.)\s|\n', text)

    current_message = ''
    for sentence in sentences:
        # Проверяем длину текущего сообщения с добавленным предложением
        if len(current_message) + len(sentence) > max_length:
            # Если превышает максимальную длину, отправляем текущее сообщение
            parts = current_message.split('\n')

            for part in parts[:-1]:  # Для всех частей, кроме последней
                text_area.send_keys(part)  # Отправка части текста
                text_area.send_keys(Keys.SHIFT, Keys.ENTER)  # Нажатие Shift+Enter

            text_area.send_keys(parts[-1])  # Отправка последней части текста
            text_area.send_keys(Keys.ENTER)  # Нажатие Enter
            # text_area.send_keys(current_message)
            # text_area.send_keys(Keys.SHIFT, Keys.ENTER)
            logger.info("Отправил часть сообщения")
            sleep(1)
            current_message = sentence  # Начинаем новое сообщение
        else:
            # Если нет, добавляем предложение к текущему сообщению
            current_message += sentence

    # Отправляем оставшееся сообщение
    if current_message:
        parts = current_message.split('\n')

        for part in parts[:-1]:  # Для всех частей, кроме последней
            text_area.send_keys(part)  # Отправка части текста
            text_area.send_keys(Keys.SHIFT, Keys.ENTER)  # Нажатие Shift+Enter

        text_area.send_keys(parts[-1])  # Отправка последней части текста
        text_area.send_keys(Keys.ENTER)  # Нажатие Enter
        #text_area.send_keys(current_message)
        logger.info("Заполнил сообщение")
        sleep(1)
        text_area.send_keys(Keys.ENTER)  # Нажатие Enter для отправки сообщения


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
    # text_area.send_keys(text)
    # logger.info("Заполнил сообщение")
    # sleep(1)
    # #send_button = w1.is_it_on_the_page("chat_send_button")
    # """if not send_button:
    #     logger.info("Нет кнопки отправки сообщения")
    #     return "No send button"""
    # text_area.send_keys(Keys.RETURN)
    # #send_button.click()
    # logger.info("Отправил сообщение")

    send_text_with_shift_enter(text_area, text)
    sleep(1)
    return "OK"
        

