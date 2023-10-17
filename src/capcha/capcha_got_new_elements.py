from logging import getLogger
from src.log_scripts import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def capcha_got_new_elements(elements):
    # Проверка на Stale Element
    not_got = 0
    for element in elements:
        try:
            _ = element.get_attribute('tag_name')
        except Exception as e:
            not_got += 1
            logger.info(f"Элемент был изменен или удален. {e}")
    return not_got > 0