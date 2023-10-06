from logging import getLogger
from src.log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

def parse_answer(s):
    logger.info("Парсинг ответа")
    # Remove 'click:' part and split the string into substrings
    substrings = s.replace('click:', '').split('/')
    
    # Convert each substring into an integer and add to list
    numbers = [int(substring) for substring in substrings]
    # Convert each substring into an integer and add to list
    numbers = [int(substring) for substring in substrings]
    logger.info("Ответ распарсен")
    return numbers


if __name__ == '__main__':
    s1 = 'click:1/6/7'
    s2 = 'click:2/5/6/9'
    print(parse_answer(s1)[2])  # Prints: [1, 6, 7]
    print(parse_answer(s2)[2])  # Prints: [2, 5, 6, 9]
