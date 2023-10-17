
from time import sleep
from logging import getLogger
from random import random #, randint
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Safari

#from src.sound import pik
from src.log_scripts import set_logger
from src.gpt import gpt
#from otklik.click import click

from .chouse_avtootklik_text import chouse_avtootklik_text
from .click import click
from .is_it_on_the_page import WebScraper

#from selenium.webdriver.common.by import By


#from webdriver.scroll import scroll_down
#from constants.dict import dict_otklik

#from constants.texts import answer1
#from configuration.read_strings_from_file import read_strings_from_file
#from pyperclip import copy, paste
"""import pyautogui

# Нажимаем сочетание клавиш Command + V
pyautogui.hotkey('command', 'v')"""

logger = getLogger(__name__)
logger = set_logger(logger)

def filling_the_card(driver: Safari, id: str, all_text:str, w3: WebScraper, all_text_to_gpt_with_numbers, sql) -> bool:    

    logger.info("Заполнение формы отклика на карточке %s", id)
    # textarea заполняется через js
    actions = ActionChains(driver)
    
    
    #logger.error("Не удалось найти автоотклик на карточке %s", id)
    texteria = w3.is_it_on_the_page("textarea")
    if texteria:
        text_gpt = ""
        
        try:
            text_gpt = gpt(all_text, id,all_text_to_gpt_with_numbers, timeout=240, sql = sql)
            #text_gpt =chouse_avtootklik_text("text")
            if text_gpt is None:
                raise Exception("Не удалось получить текст от gpt")
                #return False                                                                #!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #pik()
            sleep(2)
            driver.execute_script("arguments[0].value = arguments[1];", texteria, text_gpt)
            
            sleep(2)
            texteria.send_keys(" ")
            logger.info("Отклик заполнен gpt на карточке %s", id)
        except Exception as e:
            avtootklik = w3.is_it_on_the_page("first_avtootklik")
            logger.warning("Не удалось получить текст от gpt на карточке %s Error %s", id, e)
            if avtootklik:
                try:
                    driver.execute_script("arguments[0].focus();", avtootklik)
                    sleep(0.2)
                    click(avtootklik, driver, buttomtype="otklik1")
                    #actions.move_to_element(avtootklik).perform()
                    #avtootklik.send_keys(Keys.RETURN)
                    #avtootklik.click()
                    logger.info("Выбран автоотклик на карточке %s", id)
                except Exception as e:
                    logger.warning("Не удалось выбрать автоотклик на карточке %s Error %s", id, e)
                    try:
                        texteria.send_keys(chouse_avtootklik_text("text"))
                        logger.info("Отклик заполнен через js на карточке %s", id)
                    except Exception as e:
                        logger.error("Не удалось найти автоотклик на карточке%s", id)
                        return False
            else:
                try:
                    texteria.send_keys(chouse_avtootklik_text("text"))
                    logger.info("Отклик заполнен через js на карточке %s", id)
                except Exception as _:
                    logger.error("Не удалось найти автоотклик на карточке%s", id)
                    return False

    
    
    sleep(0.5 + random())
    logger.info("Выбор цены на карточке %s", id)
    price_conteiner = w3.is_it_on_the_page("price_conteiner2")
    if not price_conteiner:
        logger.error("Не удалось найти контейнер цены на карточке %s", id)
        return False
    w4 = WebScraper(price_conteiner, "dict_otklik")
    price_input = w4.is_it_on_the_page("price_input")
    div_price_dur = w3.is_it_on_the_page("duration_chois_conteiner")
    
    if not price_input or not div_price_dur:
        logger.error("Не удалось найти поле цены %s или продолжительности %s на карточке %s", str(price_input), str(div_price_dur), id)
        return False
    if price_input.get_attribute("value") == "6000":
        logger.info("Цена уже заполнена на карточке %s", id)
        return True
    #scroll_down(driver, 1, 2000)
    driver.execute_script("arguments[0].scrollIntoView();", price_input)
    #actions.move_to_element(price_input).perform()
    #price_input.click()
    price_input.send_keys("6000")
    logger.info("Цена заполнена на карточке %s", id)
    driver.execute_script("arguments[0].focus();", div_price_dur)
    sleep(0.1)
    driver.execute_script("arguments[0].scrollIntoView();", div_price_dur)
    actions.move_to_element(div_price_dur).perform()
    div_price_dur.click()
    logger.info("Контейнер продолжительности найден на карточке %s", id)
    logger.info("Выбор продолжительности на карточке %s", id)
    sleep(1.5 + random())
    w5 = WebScraper(driver, "dict_otklik")
    p_90 = w5.is_it_on_the_page("duration_90")
    if not p_90:
        logger.error("Не удалось найти продолжительность на карточке %s", id)
        return False
    driver.execute_script("arguments[0].focus();", p_90)
    sleep(0.1)
    
    actions.move_to_element(p_90).perform()
    p_90.click()
    logger.info("Все заполнено на карточке %s", id)    
    return True