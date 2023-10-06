# Description: Get all elements from capcha
#from selenium.webdriver.common.by import By
from logging import getLogger
#from capcha.take_screenshot import take_screenshot
from src.log_scripts.set_logger import set_logger
from src.otklik.is_it_on_the_page import  WebScraper

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def capcha_get_elements(capcha):
    logger.info("Получение элементов капчи")
    capcha_elements_scraper = WebScraper(capcha, "dict_capcha")
    capcha_elements = capcha_elements_scraper.is_it_on_the_page("capcha_elements", only_one=False) #????
    """i = 0
    for element in capcha_elements:
        i += 1
        take_screenshot(element, name = f"capcha_element_{i}.png")"""
    logger.info("Элементы капчи получены")
    return capcha_elements