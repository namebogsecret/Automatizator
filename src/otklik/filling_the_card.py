from logging import getLogger
from otklik.click import click
from sound.pik import pik
from log_scripts.set_logger import set_logger
#from otklik.click import click
from time import sleep
from otklik.chouse_avtootklik_text import chouse_avtootklik_text
from random import random , randint
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Safari
from otklik.is_it_on_the_page import WebScraper
#from webdriver.scroll import scroll_down
#from constants.dict import dict_otklik
from gpt.gpt import gpt
#from constants.texts import answer1
#from configuration.read_strings_from_file import read_strings_from_file
#from pyperclip import copy, paste
import os
"""import pyautogui

# Нажимаем сочетание клавиш Command + V
pyautogui.hotkey('command', 'v')"""

logger = getLogger(__name__)
logger = set_logger(logger)

# Кастомное исключение для GPT
class GPTException(Exception):
    pass

def write_to_log_file(text, id):
    if not os.path.exists("log_texts"):
        os.mkdir("log_texts")
    with open(f"log_texts/{id}.txt", "a") as f:
        f.write(f"{text}\n")

def fill_text_field(id, texteria, text_gpt, driver):
    try:
        driver.execute_script("arguments[0].value = arguments[1];", texteria, text_gpt)
        write_to_log_file("1", id)
        sleep(15)
        texteria.send_keys(" ")
        write_to_log_file("2", id)
        #logger.info(f"Отклик заполнен gpt на карточке {id}")
        return True
    except Exception as e:
        write_to_log_file(f"3 {e}", id)
        #logger.warning(f"Не удалось вставить текст от GPT: {e}")
        return False

def process_card(id, w3, all_text, all_text_to_gpt_with_numbers, sql, driver):
    texteria = w3.is_it_on_the_page("textarea")
    write_to_log_file("0", id)
    naputstvie = None
    if not texteria:
        write_to_log_file("4", id)
        logger.error(f"Не найден элемент textarea на карточке {id}")
        write_to_log_file("5", id)
        return False, naputstvie
    
    try:
        text_gpt, naputstvie = gpt(all_text, id, all_text_to_gpt_with_numbers, timeout=240, sql=sql)
        write_to_log_file(f"6 {text_gpt}", id)
        if text_gpt is None:
            write_to_log_file("7", id)
            raise GPTException("Не удалось получить текст от GPT")
        
        if fill_text_field(id, texteria, text_gpt, driver):
            write_to_log_file("8", id)
            return True, naputstvie

    except (GPTException, Exception) as e:
        #logger.warning(f"Не удалось получить текст от GPT на карточке {id}. Ошибка: {e}") #Ошибка: 'str' object has no attribute 'get'
        write_to_log_file(f"9 {e}", id)
        # Процесс автоотклика, если GPT не сработал
        avtootklik = w3.is_it_on_the_page("first_avtootklik")
        if avtootklik:
            write_to_log_file("10", id)
            try:
                texteria.clear()
                write_to_log_file("11", id)
                click(avtootklik, driver, buttomtype="otklik1")
                write_to_log_file("12", id)
                #logger.info(f"Выбран автоотклик на карточке {id}")
                return True, naputstvie
            except Exception as e:
                write_to_log_file(f"13 {e}", id)
                #print(e)
                #logger.warning(f"Не удалось выбрать автоотклик на карточке {id}. Ошибка: {e}")

        #logger.error(f"Не удалось обработать карточку {id}")
        return False, naputstvie


def filling_the_card(driver: Safari, id: str, all_text:str, w3: WebScraper, all_text_to_gpt_with_numbers, sql) -> bool:    
    naputstvie = None
    #logger.info("Заполнение формы отклика на карточке %s", id)
    # textarea заполняется через js
    actions = ActionChains(driver)
    write_to_log_file("00", id)
    card_processed, naputstvie = process_card(id, w3, all_text, all_text_to_gpt_with_numbers, sql, driver)
    write_to_log_file("000", id)
    if not card_processed:
        write_to_log_file("0000", id)
        return False, naputstvie
    
    sleep(0.5 + random())
    #logger.info("Выбор цены на карточке %s", id)
    price_conteiner = w3.is_it_on_the_page("price_conteiner2")
    write_to_log_file("00000", id)
    if not price_conteiner:
        write_to_log_file("000000", id)
        logger.error("Не удалось найти контейнер цены на карточке %s", id)
        return False, naputstvie
    w4 = WebScraper(price_conteiner, "dict_otklik")
    price_input = w4.is_it_on_the_page("price_input")
    div_price_dur = w3.is_it_on_the_page("duration_chois_conteiner")
    
    if not price_input or not div_price_dur:
        logger.error("Не удалось найти поле цены %s или продолжительности %s на карточке %s", str(price_input), str(div_price_dur), id)
        return False, naputstvie
    if price_input.get_attribute("value") == "6000":
        #logger.info("Цена уже заполнена на карточке %s", id)
        return True, naputstvie
    #scroll_down(driver, 1, 2000)
    driver.execute_script("arguments[0].scrollIntoView();", price_input)
    #actions.move_to_element(price_input).perform()
    #price_input.click()
    price_input.send_keys("6000")
    #logger.info("Цена заполнена на карточке %s", id)
    driver.execute_script("arguments[0].focus();", div_price_dur)
    sleep(0.1)
    driver.execute_script("arguments[0].scrollIntoView();", div_price_dur)
    actions.move_to_element(div_price_dur).perform()
    div_price_dur.click()
    #logger.info("Контейнер продолжительности найден на карточке %s", id)
    #logger.info("Выбор продолжительности на карточке %s", id)
    sleep(1.5 + random())
    w5 = WebScraper(driver, "dict_otklik")
    p_90 = w5.is_it_on_the_page("duration_90")
    if not p_90:
        #logger.error("Не удалось найти продолжительность на карточке %s", id)
        return False, naputstvie
    driver.execute_script("arguments[0].focus();", p_90)
    sleep(0.1)
    
    actions.move_to_element(p_90).perform()
    p_90.click()
    #logger.info("Все заполнено на карточке %s", id)    
    return True, naputstvie