from src.otklik.get_page import get_page
from src.otklik.is_it_on_the_page import WebScraper
from logging import getLogger
from src.log_scripts.set_logger import set_logger
from src.stata.ostalos_number_from_text import extract_number_before_today

logger = getLogger(__name__)
logger = set_logger(logger)

def get_ostalos(driver) -> str:
    current_url = driver.current_url
    url = "https://profi.ru/backoffice/a.php?z=p"
    if not get_page(driver, url):
        logger.error("Не удалось перейти на страницу")
        get_page(driver, current_url)
        return None
    
    ww = WebScraper(driver, "dict_otklik")
    ostalos = ww.is_it_on_the_page("ostalos")

    if not ostalos:
        logger.error("Нет поля с осталось")
        get_page(driver, current_url)
        return None

    ostalos = ostalos.text

    if "сегодня" not in ostalos:
        logger.error("Ошибка в получении осталось со страницы")
        get_page(driver, current_url)
        return None

    #находим число перед словом "сегодня"
    ostalos = extract_number_before_today(ostalos)

    if not ostalos:
        logger.error("Ошибка в получении осталось из текста")
        get_page(driver, current_url)
        return None
    get_page(driver, current_url)
    return ostalos