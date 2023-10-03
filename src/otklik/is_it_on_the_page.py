
from selenium.webdriver import Safari
#from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from logging import getLogger
from typing import Dict, List, Union
from log_scripts.set_logger import set_logger
#from constants.dict import dict_otklik
from constants.dicts_def import dicts
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = getLogger(__name__)
logger = set_logger(logger)

class WebScraper:
    def __init__(self, driver, dictionary = None):
        self.driver = driver
        self.dictionary = dictionary

    def is_it_on_the_page(self,  value: str, dict: str = "", only_one: bool = True, click = False) -> Union[bool, List [WebElement], WebElement]:
        if dict == "":
            if self.dictionary is not None:
                dict = self.dictionary
            else:
                #поиск по всем словарям и возврат первого найденного элемента
                for dict in dicts:
                    if value in dicts[dict]:
                        break
        value, by = dicts[dict][value]
        try:
            if by == 'css':
                method = By.CSS_SELECTOR
                selector = f"[class$='{value}']"
            elif by == 'fullcss':
                method = By.CSS_SELECTOR
                selector = f"[class='{value}']"
            elif by == 'tag':
                method = By.TAG_NAME
                selector = value
            elif by == 'xpath':
                method = By.XPATH
                selector = value
            elif by == 'id':  # Add support for searching by id
                method = By.ID
                selector = value
            elif by == 'type':
                method = By.CSS_SELECTOR
                selector = f"[type='{value}']"
            else:
                raise ValueError(f'Некорректное значение аргумента by: {by}')
        
            if only_one:
                if click:
                    element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((method, selector)))
                    element.click()
                    return element
                else:
                    return self.driver.find_element(method, selector) 
            else:
                if click: #one
                    element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((method, selector)))
                    element.click()
                    return element
                else:
                    return self.driver.find_elements(method, selector)

        except:
            logger.debug("Элемент %s не найден на странице.", value)
            return False