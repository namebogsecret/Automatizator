
#/src/parsing_cards/get_all_cards.py

from logging import getLogger
#from bs4 import BeautifulSoup

from src.log_scripts import set_logger
from src.otklik import WebScraper

logger = getLogger(__name__)
logger = set_logger(logger)
class CardGetter:
    def __init__(self, driver):
        self.driver = driver
        self.webscraper = WebScraper(driver, "dict_card_in_list")
        
    def get_all_cards(self):
        cards = []
        try:
            all = self.webscraper.is_it_on_the_page('content')
            logger.info('Элемент div с id="content-content" найден')
            if all:
                all_scraper = WebScraper(all, "dict_card_in_list",)
                get_all_cards = all_scraper.is_it_on_the_page('all_cards', only_one = False)
                if not get_all_cards:
                    logger.warning('Элемент div с id="content-content" не найден. None')
                    return []
                if not isinstance(get_all_cards, list):
                    logger.warning('Элемент div с id="content-content" не найден. not list')
                    return []
                #remove all cards with id="stories"
                for card in get_all_cards:
                    if card.get_attribute('id') != 'stories':
                        cards.append(card)
            else:
                pass
                logger.warning('Элемент div с id="content-content" не найден. None')
        except Exception as e:
            logger.warning('Элемент div с id="content-content" не найден. Error: %s', str(e))
            cards = []

        return cards