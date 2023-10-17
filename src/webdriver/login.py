
#/src/webdriver/login.py
"""Login to the website using the provided username and password. """

from random import randint
from time import sleep
from logging import getLogger
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from src.log_scripts import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def login(driver, username, password):
    forms = driver.find_elements(By.TAG_NAME,"form")
    form = forms[0]
    #take_screenshot(driver, form)
    input_fields = form.find_elements(By.TAG_NAME,"input")
    username_field = input_fields[0]
    logger.debug('Username field: %s', username_field)
    password_field = input_fields[1]
    logger.debug('Username field: %s', username_field)
    username_field.send_keys(username)
    logger.debug('sent username: %s', username)
    sleep(7+ randint(-2, 2))
    password_field.send_keys(password)
    
    sleep(4+ randint(-1, 1))

    # Submit the form
    password_field.send_keys(Keys.RETURN)
    logger.debug("sent password")
    sleep(3+ randint(-1, 1))
    #form.submit()
    logger.debug("form submitted")
    # Wait for the page to load using an explicit wait for up to 1000 seconds
    #wait = WebDriverWait(driver, 1000)
    sleep(10+ randint(-3, 3))
    return driver
