# This file contains the function that clicks the capcha elements
#import webelement
from logging import getLogger
from random import shuffle, uniform, random
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver as webdriver
#from selenium.webdriver.common.action_chains import ActionChains

from src.log_scripts import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

"""def smooth_mouse_movement(driver, start_element, end_element, steps=10):
    # Получение координат начальной и конечной точки
    start_x = start_element.location['x'] + start_element.size['width'] / 2
    start_y = start_element.location['y'] + start_element.size['height'] / 2
    
    # Выбор случайной точки в пределах конечного элемента для клика
    end_x = end_element.location['x'] + uniform(0, end_element.size['width'])
    end_y = end_element.location['y'] + uniform(0, end_element.size['height'])
    
    actions = ActionChains(driver).move_by_offset(-start_x, -start_y)  # Сброс 
    текущего положения

    step_x = (end_x - start_x) / steps
    step_y = (end_y - start_y) / steps
    
    for _ in range(steps):
        actions.move_by_offset(step_x, step_y)#.perform()
        sleep(uniform(0.05, 0.2))

    actions.perform()
    end_element.click()"""

def click_capcha_elements(capcha_elements: webdriver, capcha_solved):
    shuffle(capcha_solved)

    """# Создание начального "виртуального" элемента (в центре экрана) для 
    старта движения мыши
    previous_element = type('', (), {})()  # Простой объект для имитации WebElement
    previous_element.location = {'x': 120, 'y': 210}  # предполагается экран 1920x1080
    previous_element.size = {'width': 0, 'height': 0}"""

    for solved in capcha_solved:
        current_element = capcha_elements[solved-1]
        current_element.click()
        #smooth_mouse_movement(current_element, previous_element, current_element)
        
        # Случайная задержка перед следующим движением
        sleep(uniform(0.5, 2))

        #previous_element = current_element
    return True


def click_capcha_elements2(capcha_elements: webdriver, capcha_solved):
    logger.info("Клик по капче")
    shuffle(capcha_solved)
    for soleved in capcha_solved:
        capcha_elements[soleved-1].click()
        sleep(1+random())

    logger.info("Клик по капче успешен")
    return True