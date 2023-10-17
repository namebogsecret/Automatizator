#/src/otklik/click.py
from logging import getLogger
from random import random
from time import sleep
from time import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains

from src.log_scripts import set_logger
#from src.mouse import mouth_click
#from src.configuration import read_strings_from_file

from .get_coordinates_of_element import global_location

logger = getLogger(__name__)
logger = set_logger(logger)

def click(element: WebElement, driver:Chrome, num:int = 1, buttomtype = None) -> bool:
    logger.info("Начало клика")
    # блокирование мыши
    #Quartz.CGAssociateMouseAndMouseCursorPosition(False)
    
    
    x,y = global_location(element, driver)
    logger.info("Координаты клика: (%s, %s)", x, y)
    clicked = False
    for l in range(num):
        try:
            sleep(1)
            element.click()
            clicked = True
        except Exception as e:
            try:
                driver.execute_script("arguments[0].click();", element)
                clicked = True
            except Exception as e:
                try:
                    if buttomtype == None:
                        continue #ButtonStyles__Label-sc-1nuwmcp-4 kurYnT
                    
                    el = ""
                    if buttomtype == "button2":
                        el = ".Tariffs__Button-sc-1k10cte-2.chpKsZ"
                    if buttomtype == "button3":
                        el = ".ButtonStyles__Label-sc-1nuwmcp-4.kurYnT"
                    if buttomtype == "otklik1":
                        el = ".backoffice-common-list-item__text-container"
                    if el == "":
                        continue
                    click_element_js = f"""
                    var element = document.querySelector('"""+ el +"""');
                    var event = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                    });
                    element.dispatchEvent(event);
                    """
                    driver.execute_script(click_element_js)
                    clicked = True
                except Exception as e:
                    logger.error(f"Клик не удался {str(e)}")
                    clicked = False#mouth_click(x,y) 
        sleep(1)
     
    #clicked = mouth_click(x,y+30) 
    if clicked:
        logger.info("Конец клика 1")
        # разблокирование мыши
        timer_stop = time()
        #driver.save_screenshot(f"screenshot_{timer_stop}.png")
        return True
    else:
        logger.error("Клик 1 не удался")
        #Quartz.CGAssociateMouseAndMouseCursorPosition(False)
        clicked = click_old(element, driver)
        #Quartz.CGAssociateMouseAndMouseCursorPosition(True)         
        if clicked:
            logger.info("Конец клика 2")
            # разблокирование мыши
            timer_stop = time()
            #driver.save_screenshot(f"screenshot_{timer_stop}.png")
            return True
        else:
            logger.error("Клик2 не удался")
            timer_stop = time()
            #driver.save_screenshot(f"screenshot_{timer_stop}.png")
            return False
        

def click_old(element: WebElement, driver: Chrome) -> bool:
    try:
        action = ActionChains(driver)
        # Имитация наведения мышью на элемент
        #input("Press Enter to continue... Begining of click function. starting move to element")
        #action.move_to_element(element).perform()
        logger.info("Наведение мышью на элемент")
        # Получение списка доступных логов
        #logs = driver.execute_script('return console.log')
        sleep(0.2+ random())
        #driver.execute_script("arguments[0].focus();", element)
        #logger.info("Логи после наведения и фокус %s", str(logs))
        sleep(0.2+ random())
        action.move_to_element(element).click(element).perform()
        logger.info("Клик 1")
        
        sleep(0.2+ random())
        return True
    except Exception as e:
        logger.error("Клик2_ не удался %s", str(e))
        return False
   
    """element.click()
    logger.info("click")
    time.sleep(5)
    action.double_click(element).perform()
    logger.info("Клик 2")
    time.sleep(5)
    #driver.execute_script("arguments[0].click();", element)"""

    #logger.info("Логи после клика %s", str(logs))
    #onclick_attribute = element.get_attribute("onclick")
    #logger.info("onclick атрибут %s", str(onclick_attribute))
    # Выполняем JavaScript-код из атрибута "onclick"
    #driver.execute_script(onclick_attribute)
    # Вывод списка логов
    

    """actions = ActionChains(driver)
    driver.execute_script("arguments[0].focus();", otklik)
    time.sleep(0.1)
    actions.move_to_element(otklik).perform()
    otklik.click()
    
    actions.double_click(otklik).perform() 
    #element = driver.find_element_by_id('my-element')
    driver.execute_script("arguments[0].click();", otklik)
    '''---logs = driver.get_log('browser')
    logs.str = str(logs)---'''
    """