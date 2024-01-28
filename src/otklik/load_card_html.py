#/src/otklik/load_card_html.py
from logging import getLogger
from random import randint, random
from re import sub

from otklik.filling_the_card import filling_the_card
from text_process.podhodit import podhodit
from otklik.click import click
from os import makedirs
from os.path import exists

from time import sleep
from log_scripts.set_logger import set_logger
#from constants.texts import answer1
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
#from sound.pik import pik
from otklik.is_it_on_the_page import WebScraper
#from selenium.webdriver.common.by import By
#from constants.dict import dict_otklik
from otklik.get_id_from_url import get_id_from_url
from otklik.get_page import get_page
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement
from configuration.read_strings_from_file import read_strings_from_file
import time
from dialog.testing_send_message import testing_send_message

from database.add_message import add_message
from utils.web_hook import WebhookSender

logger = getLogger(__name__)
logger = set_logger(logger)


def wait_for_jquery_ajax(driver, max_delay_seconds=30):
    delay = max_delay_seconds
    while delay > 0:
        time.sleep(1)
        jquery = driver.execute_script("return window.jQuery == undefined;")
        if jquery:
            break
        ajax_is_complete = driver.execute_script("return window.jQuery.active == 0;")
        if ajax_is_complete:
            break
        delay -= 1

def load_card_html(url, driver, sql) -> tuple:
    strings_dict = read_strings_from_file()
    url2 = strings_dict["second_url"]
    messages = [None] * 3 
    messages[1] = strings_dict["final_frase1"]
    messages[2] = strings_dict["final_frase2"]
    ban = False
    limit = False
    html_choose = ""
    html = ""
    html_otklik_param = ""
    all_text = ""
    id = get_id_from_url(url)
    
    if not get_page(driver, url):
        return "Error", html, html_choose, html_otklik_param, all_text, ban, limit
    #html = driver.page_source
    #actions = ActionChains(driver)
    # Настройка явного ожидания на 10 секунд
    #wait = WebDriverWait(driver, 10)
    logger.info("Загрузка карточки %s url: %s", id, url)
    sleep(3 + random())
    w1 = WebScraper(driver, "dict_otklik")
    # Find element by class ending with 'faTkYO'
    if w1.is_it_on_the_page("chat_page"):
        logger.info("%s Не та страница, есть чат", id)
        return "Allready", html, html_choose, html_otklik_param, all_text, ban, limit
    all_card = w1.is_it_on_the_page("have_card")
    html = driver.page_source
    if not all_card:
        logger.error("%s Не та страница, нет чата.", id)

        return "Error", html, html_choose, html_otklik_param, all_text, ban, limit
    soup = BeautifulSoup(all_card.get_attribute('outerHTML'), 'html.parser')
    separator = ' \n '  # You can use any separator you like
    text_parts = []
    for tag in soup.find_all(text=True):
        stripped_text = tag.strip()
        if stripped_text:
            text_parts.append(stripped_text)
    all_text_to_gpt_with_numbers = separator.join(text_parts)
    # находим все цифры, кроме тех, которые стоят перед словом "класс"
    pattern = r"\b\d+(?!\s*класс)"

    # заменяем найденные цифры на пустую строку
    all_text_to_gpt = sub(pattern, "", all_text_to_gpt_with_numbers)
    soup.decompose()
    all_text = all_card.text.lower()
    if not podhodit(all_text):
        logger.info("%s не подходит", id)
    
        return "Nepodhodit", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    if w1.is_it_on_the_page("card_censeled"):
        logger.info("Карточка %s отклик отменен", id)
        return "Deleted", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    if w1.is_it_on_the_page("knopka_vakansii"):
        logger.info("%s Не та страница, есть кнопка вакансии", id)
        return "Vakans", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    uvedomlenie = w1.is_it_on_the_page("est_uvedomleniya")
    if uvedomlenie:
        logger.info("%s Есть уведомления", id)
        delete_t = uvedomlenie.text
        if "ваш отклик будет" not in delete_t: #"убран" in delete_t or "удалён" in delete_t or "уже нашёл" in delete_t or "не готов" in delete_t or "скрыт" in delete_t:
            logger.info("Карточка %s временно удалена", id)
            return "Deleted", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers,   ban, limit
     

    sleep(2 )
    #versiya dlya mobilnogo
    otklik = w1.is_it_on_the_page("otklik_chouse_button") #  кнопка выбора отклика"fdEiIF", "css"],chpKsZ
    if not otklik:
        logger.info("Нет кнопки откликнуться mibile %s", id)
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit

    #pik()    
    sleep(1)
    if not click(otklik, driver, 1):
        logger.info("Не получилось нажать на кнопку откликнуться mibile %s", id)
        html = driver.page_source
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    
    sleep(randint(2, 3))
    
    #Проверка, что мы еще не откликнулсиь на эту карточку
    if not driver.current_url.startswith(url2):
        logger.info("Оказались не на странице карточки  %s", id)
        html = driver.page_source
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    
    w2 = WebScraper(driver, "dict_otklik")
    choos_otklik_params = w2.is_it_on_the_page("choos_otklik_params")
    if choos_otklik_params:
        html_otklik_param = choos_otklik_params.get_attribute('outerHTML')
    otklik = w2.is_it_on_the_page("otklik_button") # первый вариант отклика
    if not otklik:
        logger.info("Нет вариантов отклика mibile %s", id)
        
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers  , ban, limit
    
    if otklik.text == "Отклик":
        limit_ = w2.is_it_on_the_page("day_limit")
        if limit_:
            limit = True
        ban = w2.is_it_on_the_page("ban")
        if ban:
            ban = True
        if not limit and not ban:
            logger.info("Нет лимита и бана на карточке %s", id)
            return "Vakans", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
        if ban:
            logger.info("Бан на карточке %s", id)
            return "Ban", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
        elif "50 раз" in limit_.text:
            logger.info("Лимит на карточке %s", id)
            return "Limit", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit  
        else:
            logger.info("Вакансия на карточке %s", id)
            return "Vakans", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    if otklik.text != "Комиссия":
        logger.info("Нет кнопки откликнуться после выборов %s", id)
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    
    #wait_for_jquery_ajax(driver)

    w9 = WebScraper(driver, "dict_otklik")
    #sleep(5)
    otklik = w9.is_it_on_the_page("otklik_variants_button") #,click = True) # второй вариант отклика
    #wait_for_jquery_ajax(otklik)
    if not otklik:
        logger.info("Нет кнопки отклика после выбора комиссии %s", id)
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    if type(otklik) == WebElement:
        clicked = click(otklik, driver, buttomtype="buttom3")
        if not clicked:
            logger.info("Не получилось нажать на кнопку отклика %s", id)
            html = driver.page_source
            return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    logger.info("Отклик найден, начинаю заполнение %s", id)
    

    sleep(2+ random())
    w3 = WebScraper(driver, "dict_otklik")
    html_choose = w3.is_it_on_the_page("otklik_params")
    if html_choose:
        html_choose = html_choose.get_attribute('outerHTML')
    card_filled, privetstvie, midle_text, distant_advertasing, proshanie = filling_the_card(driver, id, all_text, w3, all_text_to_gpt_with_numbers, sql)
    if not card_filled:
        logger.error("Не получилось заполнить карточку %s", id)
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    
    
    
    sleep(3+ randint(-1, 1))
    w6 = WebScraper(driver, "dict_otklik")
    button_otklik = w6.is_it_on_the_page("final_butom1")
    if not button_otklik:
        logger.info("Нет кнопки1 отправить отклик %s", id)
        button_otklik = w6.is_it_on_the_page("final_butom2")
        if not button_otklik:
            logger.info("Нет кнопки2 отправить отклик %s", id)
            return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    driver.execute_script("arguments[0].focus();", button_otklik)
    sleep(0.1)
    #button_otklik.send_keys(Keys.RETURN)
    #actions.move_to_element(button_otklik).perform() # error ButtonStyles__Label-sc-1nuwmcp-4 kurYnT
    if type(button_otklik) == WebElement:
        click(button_otklik, driver, buttomtype="buttom3")
    else:
        logger.info("Нет кнопки3 отправить отклик %s", id)
        return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    logger.info("Отклик отправлен на карточке %s", id)
    sleep(5+ randint(-2, 2))
    test_url = driver.current_url
    if not test_url.startswith(url2):
        logger.info("Отклик отправлен на карточке %s", id)
        w10 = WebScraper(driver, "dict_otklik")
        if w10.is_it_on_the_page("chat_page"):
            logger.info("Открылся чат по заказу %s, пробуем отправить доп инфо", id)
            sleep(2)
            # to_send = randint(0, 2)
            # if to_send == 0:
            #     logger.info("Не отправляем доп инфо %s", id)
            # elif to_send in [1, 2]:
            message = f"""
{privetstvie}

{midle_text}
{distant_advertasing}
{proshanie}
            """
            #messages[to_send]
            logger.info("По заказу %s Отправляем доп инфо %s", id, message)
            if not testing_send_message(driver, message):
                logger.info("Не получилось отправить доп инфо %s", id)
            else:
                start_time = time.time()
                # answers_dir = 'answers'
                # if not exists(answers_dir):
                #     makedirs(answers_dir)
                # with open(f'{answers_dir}/dop_info_{id}_{start_time}.txt', 'w') as f:
                #     f.write(message)
                add_message(sql, id, message, start_time, None, None)
            # else:
            #     logger.error("Ошибка")
        sender = WebhookSender()
        data = {
            'service': 'otklik',
            'event': 'New Otklik',
            'error': False,
            'message': f'Отклик отправлен на карточке {id}'
        }
        sender.send_webhook(data)
        return "Sent", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    html = driver.page_source
    logger.error("Отклик не отправлен на карточке %s", id)
    return "Error", html, html_choose, html_otklik_param, all_text_to_gpt_with_numbers, ban, limit
    

