"""import sys
import os
if getattr(sys, 'frozen', False):
    src_path = sys._MEIPASS
else:
    src_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(src_path)"""
import json
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
from gpt.get_user_data import get_user_data
from gpt.get_application import get_application
from functools import lru_cache

@lru_cache(maxsize=20)
def rand_int(all_text_to_gpt_with_numbers:str):
    return randint(1,9)/10

def rand_three(all_text_to_gpt_with_numbers:str):
    return randint(1,3)

def gpt(html_about:str, id: str, all_text_to_gpt_with_numbers:str, witch:int = 1, gpt4: bool = True,  temp: float = 2/10, timeout=240, sql = None):
    temp = rand_int(all_text_to_gpt_with_numbers)
    api_key = get_api()
    client4 = GPTClient(api_key, "gpt-4") #gpt-4 "gpt-4-1106-preview"
    client3 = GPTClient(api_key)
    client3_temp = 2/10
    if gpt4:
        client = client4
    else:
        client = client3
    strings_dict = read_strings_from_file()
    """user_date = None
    strings_dict = read_strings_from_file()
    report= strings_dict['report']
    try:
        get_userdate = f"''' {all_text_to_gpt_with_numbers} '''\n{report}"
        user_date, time_d = ask_gpt(client3, get_userdate, client3_temp, 210, id)
    except Exception as _:
        user_date = html_about"""
    start_time = time()
    user_date = get_user_data(html_about)
    user_date = user_date if user_date else html_about
    
    middle_one = rand_three(all_text_to_gpt_with_numbers)
    
    middle_text = strings_dict[f'midle_text_{middle_one}']
    
    
    user_date_json = json.dumps(user_date)
    application = get_application(user_date_json, middle_text, whant_distant=bool(user_date.get("remote", False)), temperature=temp)
    privetstvie = application.get("privetstvie", None)
    distant_advertasing = application.get("distant_advertasing", None)
    proshanie = application.get("proshanie", None)
    naputstvie = application.get("naputstvie", None)
    write_answer_to_file(start_time, f"""{privetstvie}
{middle_text}
{distant_advertasing}
{proshanie}""",
temp,
time() - start_time,
id,
sql = sql)
    return privetstvie, middle_text, distant_advertasing, proshanie, naputstvie
    # request1 = get_request1(witch, user_date, midle_text = midle_text)
    # answer1, time_dur = ask_gpt(client, request1, temp, timeout, id)
    # request2 = get_request2(witch, user_date, midle_text = f"{answer1} \n {midle_text}")
    # answer2, time_dur = ask_gpt(client, request2, temp, timeout, id)
    # start_time = time()
    # write_answer_to_file(start_time, f"{answer1}\n{midle_text} {answer2}", temp, time_dur, id, sql = sql)
    # return f"{answer1}\n{midle_text} {answer2}"

    #request = get_request(witch, user_date)

    #answer, time_dur = ask_gpt(client, request, temp, timeout, id)
    #start_time = time()
    #write_answer_to_file(start_time, f"{answer}", temp, time_dur, id, sql = sql)
    #return answer
