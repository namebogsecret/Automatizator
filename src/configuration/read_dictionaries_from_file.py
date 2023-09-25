import json
from typing import Dict, List, Tuple
from logging import getLogger
from log_scripts.set_logger import set_logger
from os.path import exists
from constants.dicts_def import dicts
logger = getLogger(__name__)
logger = set_logger(logger)

def read_dictionaries_from_file(filename: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]], Dict[str, List[str]]]:
    global dicts
    try:
        if not exists(filename):
            logger.error("Файл со словарями не найден")
            return {}, {}, {}, {}
        with open(filename, 'r') as file:
            data = json.load(file)
        dicts['dict_otklik'] = data['dict_otklik']
        dicts['dict_card_in_list'] = data['dict_card_in_list']
        dicts['dict_chat_status'] = data['dict_chat_status']
        dicts['dict_capcha'] = data['dict_capcha']
        return dicts['dict_otklik'], dicts['dict_card_in_list'], dicts['dict_chat_status'], dicts['dict_capcha']
    except Exception as e:
        print (data)
        logger.error(e)
        logger.error("Не удалось прочитать словари из файла")
        return  {}, {}, {}, {}
    
    
    #return dict_otklik, dict_card_in_list, dict_chat_status

if __name__ == '__main__':
    dict_otklik, dict_card_in_list, dict_chat_status = read_dictionaries_from_file(
        'src/configuration/dictionaries_old.json')
    #print(dict_otklik)