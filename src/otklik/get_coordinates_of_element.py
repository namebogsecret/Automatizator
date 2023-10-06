#/src/otklik/get_coordinates_of_element.py
from logging import getLogger
from src.log_scripts.set_logger import set_logger
logger = getLogger(__name__)
logger = set_logger(logger)

def local_location(element):
    # Получаем локальные координаты элемента на странице
    element_location = element.location
    logger.info("Локальные координаты элемента: (%s, %s)", element_location['x'], element_location['y'])

    return element_location['x'], element_location['y']

def local_size(element):
    # Получаем ширину и высоту элемента
    element_size = element.size
    logger.info("Размеры элемента: (%s, %s)", element_size['width'], element_size['height'])

    return element_size['width'], element_size['height']    

"""def get_safari_window(url):
    windows2 = CG.CGWindowListCopyWindowInfo(CG.kCGWindowListOptionAll | CG.kCGWindowListExcludeDesktopElements, CG.kCGNullWindowID)
    
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    logger.info("Список окон: %s", str(windows))
    for window in windows:
        logger.info("Окно: %s", str(window))
        if window.get('kCGWindowOwnerName') != 'Safari':
            logger.info("Окно не Safari")
            continue
        try:
            logger.info("Попытка получить url")
            url_field = window.get('kCGWindowBounds')['X'] + 5, window.get('kCGWindowBounds')['Y'] + 5, 240, 20
            logger.info("url_field: %s", str(url_field))
            image = Quartz.CGWindowListCreateImage(Quartz.CGRectMake(*url_field), Quartz.kCGWindowListOptionOnScreenOnly, window.get('kCGWindowNumber'), Quartz.kCGWindowImageBoundsIgnoreFraming)
            logger.info("image: %s", str(image))
            bitmap = Quartz.CGBitmapContextCreateWithData(image.data, image.width, image.height, 8, image.bytesPerRow, image.colorSpace, Quartz.kCGImageAlphaNoneSkipFirst, None, None)
            logger.info("bitmap: %s", str(bitmap))
            string = Quartz.create_string_with_bytes(bitmap.data)
            logger.info("string: %s", str(string))
            if url in string:
                return window
        except:
            pass
    return None

def get_safari_window_by_id(id):
    windows = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionAll | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)
    logger.info("Список окон: %s", str(windows))
    for window in windows:
        logger.info("Окно: %s", str(window))
        if window.get('kCGWindowOwnerName') != 'Safari':
            logger.info("Окно не Safari")
            continue
        try:
            window_id = window.get('kCGWindowNumber')
            if str(id) in str(window_id):
                return window
        except:
            pass
    return None
"""

def global_location(element, driver):
    # Получаем глобальные координаты элемента на странице
    lx, ly = local_location(element)
    sx, sy = local_size(element)
    global_x = lx + sx / 2
    global_y = ly + sy / 2
    logger.info("Глобальные координаты относительно браузера середины элемента: (%s, %s)", global_x, global_y)
    window_rect = driver.execute_script("return {left: window.screenX, top: window.screenY};")
    header_height = driver.execute_script("return window.outerHeight - window.innerHeight;")

    global_x = global_x + window_rect['left']
    global_y = global_y + window_rect['top'] + header_height
    logger.info("Глобальные координаты относительно экрана середины элемента: (%s, %s)", global_x, global_y)
    return global_x, global_y