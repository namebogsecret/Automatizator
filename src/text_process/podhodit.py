#src/text_process/podhodit.py
"""Функция, которая проверяет, подходит ли ученик"""
from logging import getLogger
from log_scripts.set_logger import set_logger
logger = getLogger(__name__)
logger = set_logger(logger)

def podhodit(all_text: str) -> bool:
    if "вакансия" in all_text:
        logger.info("Вакансия")
        return False
    if ("физик" in all_text or 
        "олимпиад" not in all_text or
        "5 класс" in all_text or 
        "6 класс" in all_text or 
        "7 класс" in all_text) and not (
            "1 курс" in all_text or 
            "2 курс" in all_text or 
            "3 курс" in all_text or 
            "4 курс" in all_text or 
            "5 курс" in all_text or 
            "6 курс" in all_text or 
            "дви по математике" in all_text or
            ("дви по физике" in all_text and
            "11 класс" in all_text)):
        logger.info("%s Нет мат олимпиад для старших классов, кроме олимпиад по физике, курсов, дви кроме дви по физике для 10 и младше", id)
        return True
    else:
        logger.info(f"%s не подходит")
        return False