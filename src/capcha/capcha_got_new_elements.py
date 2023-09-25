from logging import getLogger
from log_scripts.set_logger import set_logger

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
            loger.info(f"Элемент с индексом {i} был изменен или удален. {e}")
    return not_got > 0