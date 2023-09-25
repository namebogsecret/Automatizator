#/src/otklik/load_card_html.py
from logging import getLogger
from random import randint, random

from otklik.filling_the_card import filling_the_card
from text_process.podhodit import podhodit
from otklik.click import click

from time import sleep
from log_scripts.set_logger import set_logger
from constants.texts import answer1
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from sound.pik import pik
from .is_it_on_the_page import is_it_on_the_page
from selenium.webdriver.common.by import By
from constants.dict import dict_otklik
from otklik.get_id_from_url import get_id_from_url
from otklik.get_page import get_page
from configuration.read_strings_from_file import read_strings_from_file

logger = getLogger(__name__)
logger = set_logger(logger)

def load_card_html(url, driver):
    strings_dict = read_strings_from_file()
    url2 = strings_dict["second_url"]
    id = get_id_from_url(url)
    
    if not get_page(url, driver):
        return "Error"

    actions = ActionChains(driver)
    # Настройка явного ожидания на 10 секунд
    #wait = WebDriverWait(driver, 10)
    logger.info("Загрузка карточки %s url: %s", id, url)
    sleep(3+ random())
    # Find element by class ending with 'faTkYO'
    try:
        all_card = driver.find_element(By.CSS_SELECTOR,"[class$='hVwTNm']") #have_card
        all_text = all_card.text.lower()
        logger.info("Карточка %s найдена", id)

        if podhodit(all_text):
            logger.info("%s Нет мат олимпиад для старших классов, кроме олимпиад по физике, курсов, дви кроме дви по физике для 10 и младше", id)
        else:
            logger.info("%s не подходит", id)
            return "Nepodhodit"
    except Exception as e:
        all_card = None
        logger.info("%s Не та страница, нет самой карточки. Error: %s", id, str(e))
        try:
            chat = driver.find_element(By.CSS_SELECTOR,"[class$='jZJgbl']") #chat_page
            logger.info("%s Не та страница, есть чат", id)
            return "Allready"
        except Exception as e:
            
            logger.error("%s Не та страница, нет чата. Error: %s", id, str(e))
            return "Error"
    otklik = None
    try:
        otklik = driver.find_element(By.CSS_SELECTOR,"[class$='faTkYO']") #otklik_chouse_button
        logger.info("Есть кнопка откликнуться на карточке mobyle version %s", id)
        pik(100)
    except Exception as e:
        try:
            otklik = driver.find_element(By.CSS_SELECTOR,"[class$='huGzNf']") #otklik_button
            logger.info("есть какие-то варианты отклика на карточке desktop %s, error was: %s", id, str(e))
            pik(100)
        except Exception as e:
            logger.info("Нет кнопки откликнуться на карточке %s, error was: %s", id, str(e)) 
            try:
                vakan = driver.find_element(By.CSS_SELECTOR,"[class$='backoffice-common-button__text_theme-black']") #knopka_vakansii
                logger.info("%s Не та страница, есть кнопка вакансии", id)
                return "Vakans"
            except Exception as e:
                logger.info("%s Не та страница, нет кнопки вакансии. Error: %s", id, str(e))
                try:
                    delete = driver.find_element(By.CSS_SELECTOR,"[class$='ui-notice__text']") #est_uvedomleniya
                    #delete_str = str(delete)
                    delete_t = delete.text
                    if "убран" in delete_t or "удалён" in delete_t or "уже нашёл" in delete_t:
                        logger.info("Карточка %s временно удалена", id)
                        return "Deleted"
                    elif "ждет" in delete_t or "по рейтингу" in delete_t:

                        logger.error("Карточка %s ждет не распознало отклик", id)
                        return "Error"
                    else:
                        try:
                            cancel = driver.find_element(By.CSS_SELECTOR,"[class$='reports__order-label']") #card_censeled
                            """ if "отмен" in cancel.text:"""
                            logger.info("Карточка %s отклик отменен", id)
                            return "Deleted"
                            """else:
                                logger.error("Карточка %s непонятно что (отмена1?)!", id)
                                return "Error"""
                        except Exception as e:
                            logger.error("Карточка %s непонятно что! (Отложено?)", id)
                            return "Error"
                        
                except Exception as e:
                    try:
                        cancel = driver.find_element(By.CSS_SELECTOR,"[class$='reports__order-label']") #card_censeled
                        
                        return "Deleted"
                    except Exception as e:
                        logger.error("Не та страница и не Удалена или нет кнопки откликнуться на карточке %s. Error: %s", id, str(e))
                        return "Error"
   
    if otklik is None:
        return "Error"
    pik()    
    sleep(1)
    click(otklik, driver, 2)
    #sleep(0.1)
    #click(otklik,actions, driver)
    sleep(randint(2, 3))
    test_url = driver.current_url
        #Проверка, что мы еще не откликнулсиь на эту карточку
    if not test_url.startswith(url2):
        logger.info("Уже откликнулись на карточке %s", id)
        return "Already"
    #Проверка, что не вакансия для мобильной версии
    try:
        otklik = driver.find_element(By.CSS_SELECTOR,"[class$='huGzNf']") #otklik_button
        logger.info("Не Вакансия? на карточке %s", id)
    except Exception as e:
        logger.error("Не получилось проверить на вакансию на карточке %s. Error: %s", id, str(e))
        
    
    if not otklik.text == "Комиссия":
        try:
            limit = driver.find_element(By.CSS_SELECTOR,"[class$='dOtiyh']") #day_limit
            logger.info("проверка лимита %s", id)
            if "50 раз" in limit.text:
                logger.info("Лимит на карточке %s", id)
                return "Error"                                                  """ реализовать добавление во временные лимиты в базе данных"""
            else:
                logger.info("Вакансия на карточке %s", id)
                return "Vakans"
        except Exception as e:
            logger.error("Не получилось проверить лимит на карточке %s. Error: %s", id, str(e))
            return "Error"
    logger.info("Не Вакансия на карточке %s", id)
    
    try:
        otklik = driver.find_element(By.CSS_SELECTOR,"[class$='gjrwwU']") #otklik_variants
        click(otklik, driver, 1)
        logger.info("Отклик1  на карточке %s", id)
        #sleep(0.2)
        #click(otklik,actions, driver)
        logger.info("Отклик1  на карточке %s", id)
    except Exception as e:
        logger.error("Не получилось откликнуться на карточке %s. Error: %s", id, str(e))
        return "Error"
    sleep(2+ random())
    
    if not filling_the_card(driver, id):
        logger.error("Не получилось заполнить карточку %s", id)
        return "Error"
    
    
    
    sleep(3+ randint(-1, 1))
    try:
        button_otklik = driver.find_element(By.CSS_SELECTOR,"[class$='iGBLUs']") #final_butom1
        driver.execute_script("arguments[0].focus();", button_otklik)
        sleep(0.1)
        button_otklik.send_keys(Keys.RETURN)
        actions.move_to_element(button_otklik).perform()
        button_otklik.click()
        logger.info("Отклик отправлен на карточке %s", id)
        sleep(5+ randint(-2, 2))
        test_url = driver.current_url
        #Проверка, что мы еще не откликнулсиь на эту карточку
        if test_url.startswith(url2):
            logger.info("Не удалось нажать на отправить отклик %s", id)
            return "Error"
        else:
            logger.info("Отклик отправлен на карточке %s", id)
            return "Sent"
    except Exception as e:
        try:
            button_otklik = driver.find_element(By.CSS_SELECTOR,"[class$='gJnrsw']") #final_butom1
            driver.execute_script("arguments[0].focus();", button_otklik)
            sleep(0.1)
            button_otklik.send_keys(Keys.RETURN)
            actions.move_to_element(button_otklik).perform()
            button_otklik.click()
            logger.info("Отклик отправлен на карточке %s", id)
            sleep(5+ randint(-2, 2))
            test_url = driver.current_url
            #Проверка, что мы еще не откликнулсиь на эту карточку
            if test_url.startswith(url2):
                logger.info("Не удалось нажать на отправить отклик %s", id)
                return "Error"
            else:
                logger.info("Отклик отправлен на карточке %s", id)
                return "Sent"
        except Exception as e:
            logger.error("Не получилось отправить отклик на карточке %s. Error: %s", id, str(e))
            return "Error"

