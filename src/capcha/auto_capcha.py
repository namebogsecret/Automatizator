# -*- coding: utf-8 -*-
# Path: src/capcha/capcha_get_elements.py
# Решение капчи

"""import sys
sys.path.append("/Volumes/Untitled/Automatizator/src/")"""

import requests
import time
from configuration.read_strings_from_file import read_strings_from_file
#import base64
from logging import getLogger
from log_scripts.set_logger import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

strings_dict = read_strings_from_file()


API_KEY = strings_dict['capcha_api']
UPLOAD_URL = 'http://2captcha.com/in.php'
RESULT_URL = 'http://2captcha.com/res.php'

def auto_capcha(capcha_screenshot, instructions_screenshot):

    """with open(capcha_screenshot, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')"""
    # 1. Отправка изображения с капчей
    with open(capcha_screenshot, 'rb') as image_file:
        with open(instructions_screenshot, 'rb') as instructions_file:
            logger.info("Отправка изображения с капчей")
            response = requests.post(
                                        UPLOAD_URL,
                                        {
                                            'key': API_KEY,
                                            'method': 'post',
                                            'recaptcha': 1,
                                            'lang': 'en'
                                        },
                                        files = {
                                            'file': image_file,
                                            'imginstructions': instructions_file
                                        }
                                    )

    response_data = response.text.split('|')
    logger.info("Получение ответа")
    if response_data[0] == 'OK':
        captcha_id = response_data[1]
        logger.info("Ответ получен")
    else:
        logger.error(f"""Ошибка при загрузке изображения: 
        {response.text} {response_data} {response.content}""")
        logger.info("Ошибка при загрузке изображения")
        return None


    # 2. Ожидание решения
    time.sleep(5)

    # 3. Получение решения капчи
    for _ in range(30):  # Попытка получения ответа 10 раз с интервалом в 5 секунд
        logger.info("Получение решения капчи")
        result_response = requests.get(
            RESULT_URL,
            params={
                'key': API_KEY,
                'action': 'get',
                'id': captcha_id,
                'json': 1
            }
        )
        result_json = result_response.json()
        if result_json['request'] == 'CAPCHA_NOT_READY':

            time.sleep(5)
            logger.info(f"""Ожидание решения капчи 
            {result_json}... {result_response} {time}""")
            continue
    
    result_data = result_json['status']
    if result_data == 1:
        logger.info(f"Решение капчи получено {result_json}")
        logger.info(f"Ответ на капчу: {result_json['request']}")
        return result_json['request']
    else:
        logger.info(f"Ошибка при получении решения {result_json}")
        logger.warning(f"Ошибка при получении решения: {result_response.text}")
        return None

if __name__ == '__main__':

    print(auto_capcha('capcha.png', 'instructions.png')) #click:1/6/7