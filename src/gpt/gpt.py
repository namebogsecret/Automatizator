"""import sys
import os
if getattr(sys, 'frozen', False):
    src_path = sys._MEIPASS
else:
    src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)"""
from configuration.read_strings_from_file import read_strings_from_file
from gpt.ask_gpt import ask_gpt
#from requests import get, post
#from json import dumps, loads
#from time import time
from gpt.gptclient import GPTClient
#from constants.api import api_key as api_old
from gpt.get_request import get_request, get_request1, get_request2
from configuration.get_api import get_api
from random import randint
from time import time

from gpt.ask_gpt import write_answer_to_file

def gpt(html_about:str, id: str, all_text_to_gpt_with_numbers:str, witch:int = 1, gpt4: bool = True,  temp: float = 2/10, timeout=240, sql = None):
    temp = randint(1,9)/10
    api_key = get_api()
    client4 = GPTClient(api_key, "gpt-4")
    client3 = GPTClient(api_key)
    client3_temp = 2/10
    if gpt4:
        client = client4
    else:
        client = client3
    user_date = None
    strings_dict = read_strings_from_file()
    report= strings_dict['report']
    try:
        get_userdate = f"''' {all_text_to_gpt_with_numbers} '''\n{report}"
        user_date, time_d = ask_gpt(client3, get_userdate, client3_temp, 210, id)
    except Exception as _:
        user_date = html_about

    """middle_one = randint(1,3)
    
    midle_text = strings_dict[f'midle_text_{middle_one}']
    request = get_request1(witch, user_date)
    answer1, time_dur = ask_gpt(client, request, temp, timeout, id)
    request = get_request2(witch, user_date)
    answer2, time_dur = ask_gpt(client, request, temp, timeout, id)
    start_time = time()
    write_answer_to_file(start_time, f"{answer1} {midle_text} {answer2}", temp, time_dur, id, sql = sql)
    return f"{answer1} {midle_text} {answer2}"""

    request = get_request(witch, user_date)

    answer, time_dur = ask_gpt(client, request, temp, timeout, id)
    start_time = time()
    write_answer_to_file(start_time, f"{answer}", temp, time_dur, id, sql = sql)
    return answer

if __name__ == "__main__":
    
    html_about = 'математикаот 2800\xa0руб./чописаниеповышение успеваемостиученикандрей, 5 класс.адреспоказать картупроспект мира, 122алексеевскаяклиент может приехатьалексеевскаядетали заказа№ 55205075заказ оставлен 1 минуту назадуточнить деталиеекатерина сейчас в сетина профис 27 июля 2021подтвердиланомеротзывов от специалистов пока нетв этом заказе ваш отклик будет 1-м по рейтингу.'
    print (gpt(html_about, gpt4 = True, temp = 1))
    