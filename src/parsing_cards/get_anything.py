
#src/parsing_cards/get_anything.py
from logging import getLogger
from urllib.parse import urljoin

from src.log_scripts import set_logger
from src.configuration import read_strings_from_file

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)
strings_dict = read_strings_from_file()
second_base_url = strings_dict["second_base_url"]
base_url = second_base_url

def find_elements_by_class_suffix(soup, tag_name, suffix):
    elems = []
    for elem in soup.find_all(tag_name, class_=lambda c: c and c.endswith(suffix)):
        elems.append(elem)
    logger.debug('Elements found: ')
    return elems if elems else ["None"]

def href_from_relative_url(relative_url):
    logger.debug('Relative url done')
    return urljoin(base_url, relative_url)