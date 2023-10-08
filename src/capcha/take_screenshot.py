# Desc: Take screenshot of capcha
from PIL import Image
from io import BytesIO
from logging import getLogger
from src.log_scripts.set_logger import set_logger
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from os import makedirs
from os.path import exists

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def take_screenshot(element, name = 'screenshot'):
    try:
        logger.info(" Скриншот капчи")

        #location = element.location
        #size = element.size
        #png = driver.get_screenshot_as_png() # делаем скриншот всей страницы
        if isinstance(element, WebDriver):
            png = element.get_screenshot_as_png()
        elif isinstance(element, WebElement):
            png = element.screenshot_as_png
        else:
            raise TypeError(f"Unsupported element type: {type(element)}")
        #print (png2)
        #print (png)
        logger.info(" Скриншот капчи получен")
        captcha_dir = 'captcha'
        if not exists(captcha_dir):
            makedirs(captcha_dir)
        adress = f'{captcha_dir}/{name}.png'
        im = Image.open(BytesIO(png)) 
        logger.info(" Скриншот капчи открыт")
        im.save(adress)
        logger.info(" Скриншот капчи сохранен")
    except Exception as e:
        logger.error(f" Ошибка при получении скриншота капчи: {e}")
        adress = None
    return adress
    #im = Image.open(BytesIO(png2))
    #im.save('screenshot2.png')
    #exit()
    """left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom)) # обрезаем изображение до размеров элемента
    im.save('screenshot_capcha_.png') # сохраняем скриншот
    return 'screenshot.png' #return image_path
"""