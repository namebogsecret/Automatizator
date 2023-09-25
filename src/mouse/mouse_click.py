#/src/mouse/mouse_click.py
from time import sleep
#import Quartz.CoreGraphics as CG
from logging import getLogger
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def mouth_click(x, y):
    pass
    """try:
        logger.debug('Clicking at %s, %s', x, y)
        # переместить мышь в указанные координаты
        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(None, CG.kCGEventMouseMoved, CG.CGPointMake(x, y), CG.kCGMouseButtonLeft))
        sleep(0.2)
        logger.debug('Mouse moved to %s, %s', x, y)
        # нажать кнопку мыши
        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseDown, CG.CGPointMake(x, y), CG.kCGMouseButtonLeft))
        logger.debug('Mouse button pressed')
        sleep(0.3)
        # отпустить кнопку мыши
        CG.CGEventPost(CG.kCGHIDEventTap, CG.CGEventCreateMouseEvent(None, CG.kCGEventLeftMouseUp, CG.CGPointMake(x, y), CG.kCGMouseButtonLeft))
        logger.debug('Mouse button released')
        return True
    except Exception as e:
        logger.error('Error while clicking at %s', str(e))
        return False"""

if __name__ == '__main__':
    mouth_click(100, 100)