# Данный модуль решает капчу, если она есть на странице
from src.capcha.element_is_displayed import element_is_displayed
from src.capcha.auto_capcha import auto_capcha
from src.capcha.capcha_get_elements import capcha_get_elements
from src.capcha.take_screenshot import take_screenshot
from src.capcha.click_capcha_elements import click_capcha_elements
from src.capcha.parse_answer import parse_answer
from src.capcha.image_compresser import compress_image3
from logging import getLogger
from src.log_scripts.set_logger import set_logger
#from selenium.webdriver.common.by import By
from time import sleep, time
from random import random

from src.otklik.is_it_on_the_page import WebScraper
from src.capcha.capcha_got_new_elements import capcha_got_new_elements

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def solve_capcha(driver):
    # Предполагая, что у вас уже есть инициализированный объект Selenium `driver`
    #sitekey_element = driver.find_element_by_class_name("g-recaptcha")
    #sitekey = sitekey_element.get_attribute("data-sitekey")
    """from twocaptcha import TwoCaptcha

    solver = TwoCaptcha('YOUR_API_KEY')

    # Получить текущий URL
    current_url = driver.current_url

    result = solver.recaptcha(sitekey=sitekey, url=current_url)
    # Этот скрипт вставляет токен reCAPTCHA в скрытое поле формы, которое 
    # обычно называется "g-recaptcha-response"
    script = f'document.getElementById("g-recaptcha-response").value = 
    "{result["code"]}";'
    driver.execute_script(script)
    """
    oblovlenie = 0
    while True:
        
        capcha_scraper = WebScraper(driver, "dict_capcha")
        page_html = driver.page_source
        timestamp = str(int(time()))
        with open(f"capcha_not_cklicked_{timestamp}.html", "w") as file:
            file.write(page_html)
        logger.info("Решение капчи")
        # Проверка наличия капчи
        capcha = capcha_scraper.is_it_on_the_page("capcha_grid") 
        # rc-imageselect-target")
        logger.info("Проверка наличия капчи")
        instructions = capcha_scraper.is_it_on_the_page('capcha_instruction')
        logger.info("Проверка наличия инструкций")

        if not capcha or not instructions:
            logger.info("Капча не найдена")
            return None
        # Проверка наличия кнопки "Проверить"
        capcha_button = capcha_scraper.is_it_on_the_page("capcha_button")
        logger.info("Проверка наличия кнопки 'Проверить'")
        if not capcha_button:
            logger.info("Кнопка 'Проверить' не найдена")
            return None
        # Скриншот капчи
        capcha_screenshot = take_screenshot(capcha, f'capcha_{timestamp}')
        logger.info("Скриншот капчи")
        # Скриншот инструкций
        instructions_screenshot = take_screenshot(instructions,
         f'instructions_{timestamp}')
        logger.info("Скриншот инструкций")
        
        # Получение элементов капчи
        capcha_elements = capcha_get_elements(capcha)
        logger.info("Получение элементов капчи")
        # comress images
        capcha_screenshot = compress_image3(capcha_screenshot, max_size = (400,400))
        logger.info("Сжатие изображения капчи")
        instructions_screenshot = compress_image3(instructions_screenshot)
        logger.info("Сжатие изображения инструкций")
        # Решение капчи
        capcha_solved = auto_capcha(capcha_screenshot, instructions_screenshot)
        logger.info(f"Решение капчи {str(capcha_solved)}")
        if not capcha_solved:
            logger.warning("Капча не решена")
            #continue
            parsed_answer = []
        else:
            parsed_answer = parse_answer(capcha_solved)
        logger.info(f"Парсинг ответа {str(parsed_answer)}")
        # Клик по капче
        try:
            click_capcha_elements(capcha_elements, parsed_answer)
            logger.info("Клик по капче")
        except Exception as e:
            logger.info(f"Клик по капче не удался {e}")
        
        take_screenshot(capcha, f'capcha_solved_{timestamp}')
        # Клик по кнопке "Проверить"
        sleep(7+2*random())
        cgne = capcha_got_new_elements(capcha_elements)
        if cgne:
            logger.warning("Картинки обновились, делаем заново")
            oblovlenie += 1
            if oblovlenie < 4:
                continue
        try:
            capcha_button.click()
        except Exception as e:
            logger.info(e)
        sleep(5+2*random())
        
        try:
            take_screenshot(capcha, f'capcha_solved_li_{timestamp}')
            page_html = driver.page_source
            
            logger.info("Записан файл ошибки")
        except Exception as e:
            logger.info(f"Капча пропала занчит решена {e}")
            return True
        with open(f"capcha_cklicked_{timestamp}.html", "w") as file:
            file.write(page_html)
        try:
            capcha_scraper = WebScraper(driver, "dict_capcha")
            capcha_more = capcha_scraper.is_it_on_the_page("dynamic_more_capcha")
            incorrect_capcha = capcha_scraper.is_it_on_the_page("incorrect_capcha")
            not_all_capcha = capcha_scraper.is_it_on_the_page("not_all_capcha")
            select_any_capcha = capcha_scraper.is_it_on_the_page("select_any_capcha")
        except Exception as e:
            logger.info(f"Капча пропала 2 занчит решена {e}")
            return True
        if capcha_more:
            more = element_is_displayed(capcha_more)
            if more:
                logger.info("Картинки обновились, делаем заново")
                oblovlenie = 0
                continue
        if incorrect_capcha:
            more = element_is_displayed(incorrect_capcha)
            if more:
                logger.info("Капча неверная, делаем заново")
                oblovlenie = 0
                continue
        if not_all_capcha:
            more = element_is_displayed(not_all_capcha)
            if more:
                logger.info("Не все кликнули, делаем заново")
                oblovlenie = 0
                continue
        if select_any_capcha:
            more = element_is_displayed(select_any_capcha)
            if more:
                logger.info("Ничего не кликнули, делаем заново")
                oblovlenie = 0
                continue
        logger.info("Капча пропала занчит решена")
        sleep(5 + 2*random())
        return True
    return True