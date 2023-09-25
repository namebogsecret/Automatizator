#/src/webdriver/prepare_page.py
""" Модуль для подготовки страницы к парсингу """
from random import random
from time import sleep
#from capcha import take_screenshot
from capcha.solve_capcha import solve_capcha
from configuration.read_strings_from_file import read_strings_from_file
from otklik.is_it_on_the_page import WebScraper
from webdriver.login import login
from webdriver.scroll import scroll_down
#from selenium import webdriver
from logging import getLogger
from log_scripts.set_logger import set_logger

##from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Safari, Options
from capcha.take_screenshot import take_screenshot
from selenium.webdriver.chrome.service import Service
import json
from os.path import exists
#from selenium.webdriver.chrome import DevTools
#Safari
logger = getLogger(__name__)
logger = set_logger(logger)

def set_option(options):
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options

def prepare_page(scrolldown: int = 5):
    strings_dict = read_strings_from_file()
    url2 = strings_dict["second_url"]
    base_url = strings_dict["second_base_url"]
    my_login = strings_dict["login"]
    my_password = strings_dict["password"]
    my_driver = strings_dict["driver"]
    logger.info("Инициализация драйвера Selenium, используя браузер Safari")
    if my_driver == "chrome":
        options = ChromeOptions()
        options = set_option(options)
        #chrome_driver_path = "/usr/local/bin/chromedriver"
        #chrome_options.binary_location =
        # "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        #chrome_driver_path = "/Volumes/Untitled/Automatizator/chromedriver"
        """chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")"""
        #options = ChromeOptions()
        #options.add_argument("--headless")
        #chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        #chrome_options.binary_location =
        # "/Volumes/Cache/ProgramFiles/Google Chrome.app/Contents/MacOS/Google Chrome"
        #driver = Chrome( options=options)
        #driver = Chrome(executable_path=chrome_driver_path, options=chrome_options)

        #driver = Chrome()#Safari() /usr/local/bin/chromedriver
        driver = Chrome(options=options)
    elif my_driver == "safari":
        # Задаем уникальный идентификатор окна Safari
        options = Options()
        #options.set_capability('safari.initialUrl', 'profi_fucker')
        options = set_option(options)
        driver = Safari(options=options)
    else:
        if my_driver != "firefox":
            logger.warning("Драйвер не найден, пробуем firefox")
        options = FirefoxOptions()
        options = set_option(options)
        #gecko_driver_path = "/Volumes/Untitled/Automatizator/geckodriver"
        driver = Firefox(options=options)

    #driver.implicitly_wait(10)
    # Получение высоты экрана
    driver.set_window_position(1440,0)
    #driver.maximize_window()
    height = driver.execute_script("return window.screen.availHeight")
    # Установка размера окна браузера по вертикали
    driver.set_window_size(height/2, height-50)
    #devtools = driver.create_devtools_session()

    # Переход на URL-адрес
    while True:
        driver.get(base_url)
        if exists("cookies.txt"):
            logger.info("Файл cookies.txt найден.")

            with open('cookies.txt', 'r') as file:
                content = file.read()
                if content:  # Проверяем, не пустой ли файл
                    cookies = json.loads(content)
                    for cookie in cookies:
                        driver.add_cookie(cookie)
                else:
                    logger.info("Cookies file is empty!")
        driver.get(url2)

        # Save cookies to a file
        with open('cookies.txt', 'w') as file:
            json.dump(driver.get_cookies(), file)

        logger.info("Получение страницы")
        sleep(10+5*random())
        take_screenshot(driver, "befour_login.png")
        # Вход в систему с помощью имени пользователя и пароля
        ws = WebScraper(driver, "dict_capcha")
        login_page = ws.is_it_on_the_page("login_page")
        if not login_page:
            with open('cookies.txt', 'w') as file:
                json.dump(driver.get_cookies(), file)
            break
        driver = login(driver, my_login, my_password)
        logger.info("Вход в систему")
        ws = WebScraper(driver, "dict_capcha")
        login_page = ws.is_it_on_the_page("login_page")
        #driver.save_screenshot("screenshot_2.png")
        if not login_page:
            with open('cookies.txt', 'w') as file:
                json.dump(driver.get_cookies(), file)
            break
        cf = WebScraper(driver, "dict_capcha")
        capcha_iframe = cf.is_it_on_the_page("capcha_iframe")
        if not capcha_iframe:
            logger.info("Капча не найдена")
            with open('cookies.txt', 'w') as file:
                json.dump(driver.get_cookies(), file)
            continue
        driver.switch_to.frame(capcha_iframe)
        cc = WebScraper(driver, "dict_capcha")
        capcha = cc.is_it_on_the_page("capcha_button")
        #driver.save_screenshot("screenshot_1.png")
        if capcha:
            logger.info("Капча найдена")
            solve_capcha(driver)
            sleep(10)
            
            driver.switch_to.default_content()
            take_screenshot(driver, "login_li.png")
            ws = WebScraper(driver, "dict_capcha")
            login_page = ws.is_it_on_the_page("login_page")
            #driver.save_screenshot("screenshot_2.png")
            if login_page:
                take_screenshot(driver, "login_unsuccess.png")
                logger.warning("Не удалось войти в систему возможно капча.")
                sleep(10 + 5*random())
                take_screenshot(driver, "login_unsuccess2.png")
                with open('cookies.txt', 'w') as file:
                    json.dump(driver.get_cookies(), file)
                continue
        else:
            #take_screenshot(driver, "login_success.png")
            
            take_screenshot(driver, "login_success.png")
            logger.info("Вход в систему успешен")
            
            sleep(10 + 3*random())
            take_screenshot(driver, "login_success2.png")
            with open('cookies.txt', 'w') as file:
                json.dump(driver.get_cookies(), file)
            break
    # Прокрутка страницы 35 раз
    scroll_down(driver, scrolldown)
    logger.info("Страница готова к парсингу")
    return driver, 1440 + height/2