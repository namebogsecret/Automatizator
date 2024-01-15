from selenium.webdriver import Safari
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)


def get_page(driver: Safari, url: str) -> bool:
    def load_url():
        driver.get(url)

    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(load_url).result(timeout=30)
            return True
    except TimeoutError:
        logger.error("Error loading URL: %s. Timeout after 10 seconds.", url)
        driver.execute_script("window.stop();")  # Останавливаем загрузку страницы
        return False
    except Exception as e:
        logger.error("Error loading URL: %s. Error: %s", url, str(e))
        return False



"""
def get_page(driver: Safari,url: str) -> bool:
    try:
        driver.implicitly_wait(10)
        driver.get(url)
        driver.implicitly_wait(0)
        return True
    except Exception as e:
        logger.error("Error loading URL: %s. Error: %s", url, str(e))
        return False"""