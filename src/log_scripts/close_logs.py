
from logging import getLogger

from src.log_scripts import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

def close_log_files():
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
