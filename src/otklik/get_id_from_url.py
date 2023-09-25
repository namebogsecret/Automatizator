from logging import getLogger
from log_scripts.set_logger import set_logger

logger = getLogger(__name__)
logger = set_logger(logger)

def get_id_from_url(url: str) -> str:
    """ Получение идентификатора из URL-адреса """
    start_index = url.find('o=') + 2
    end_index = url.find('&', start_index)
    id = url[start_index:end_index]
    logger.info("Идентификатор получен из URL-адреса %s", id)
    return id