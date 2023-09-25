from parsing_cards.get_anything import href_from_relative_url
from images.img_process import get_img_url
from logging import getLogger
from log_scripts.set_logger import set_logger
from selenium.webdriver.common.by import By
from otklik.is_it_on_the_page import WebScraper
from images.save_img import save_img
#import configuration.dictionaries_old.json
from configuration.read_dictionaries_from_file import read_dictionaries_from_file
from selenium.webdriver.remote.webelement import WebElement
import re
logger = getLogger(__name__)
logger = set_logger(logger)

    
class CardProcessor3:

    def __init__(self, driver: WebElement):

        self.driver = driver
        _, self.dict, _, _ = read_dictionaries_from_file('src/configuration/dictionaries_old.json')
        self.webscraper = WebScraper(driver, "dict_card_in_list")

    def is_it_on_the_page(self, value: str):
        return self.webscraper.is_it_on_the_page(value)

    def extract_card_detail(self, card, key):
        element = self.webscraper.is_it_on_the_page(key)
        if not isinstance(element, bool) and not isinstance(element, list):
            value = element.text
        else:
            value = None

        card.update({key: value})
        logger.debug('Key: %s, Value: %s', key, value)

    def process_3(self):
        card = {}
        non = -1
        id = None

        # Используйте функцию is_it_on_the_page для поиска элементов
        url = self.is_it_on_the_page('url')
        if not isinstance(url, bool) and not isinstance(url, list):
            id = url.get_attribute('id')
            url = href_from_relative_url(url.get_attribute('href'))
        else:
            logger.error('Url not found')
            return None
        logger.debug('Href: %s', url)
        logger.debug('Id: %s', id)
        card.update({'url': url})
        card.update({"id": id})

        # Используйте функцию is_it_on_the_page и обновите остальные части кода
        for key in ['vizited', 'distant', 'school', 'modified']:
            self.extract_card_detail(card, key)

        

        
        # Обработка img1 и img2
        img1 = "None"
        img2 = "None"
        try:
            
            im_c=self.dict['img1'][0] #"gqTusJ"
            outer = self.driver.get_attribute('outerHTML')
            pattern = '<img.*?src="(.*?)".*?>'
            result = re.findall(pattern, outer)

            if result:
                #print(result)
                img1 = result[0]
                img2 = result[0]
            #else:
            #    print("Тег <img> с атрибутом src не найден на веб-странице")
                """ img1b = self.driver.find_elements(By.XPATH,f"/img[contains(@class, '{im_c}')]")
                if img1b[0] is not None:
                    img1 = img1b[len(img1b)-1].get_attribute('src')"""
        except Exception as e:
            non+=1
            img1 = "None"
            img2 = "None"
        
        card.update({"img1": img1})
        logger.debug('Img1: %s', img1)
        
        #img2 = "None"
        try:
            im_c=self.dict['img2'][0]#"hRXoKA"
            outer = self.driver.get_attribute('outerHTML')
            pattern = '<img.*?src="(.*?)".*?>'
            result = re.findall(pattern, outer)

            if result:
                #print(result)
                img2 = result[0]
        except Exception as e:
            non+=1
            #img2 = "None"
        card.update({"img2": img2})
        logger.debug('Img2: %s', img2)
        
        for img_key in ['img1', 'img2']:
            img_src = card.get(img_key)
            if img_src is not None and img_src != '' and img_src != 'None':
                pars = False
                if img_key == 'img1':
                    pars = True
                img_url = get_img_url(img_src, pars)
                card[img_key] = img_url #save_img(img_url, f"{id}_{img_key[-1]}")
            else:
                non += 1

        # Обработка остальных ключей
        for key in ['schedule', 'class_description', 'in_time', 'price', 'address', 'price_all', 'ot_do', 'subject', 'name', 'posted']:
            self.extract_card_detail(card, key)

        if non == card.__len__():
            logger.debug('Card is empty')
            return None
        else:
            logger.debug('Card is not empty')
            card.update({"html": str(self.driver)})
            return card

