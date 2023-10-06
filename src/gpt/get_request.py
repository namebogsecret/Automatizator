#from constants.texts import answer1, predistoriya, pro_clienta, instrukcii
from src.gpt.textextractor import TextExtractor
from src.configuration.read_strings_from_file import read_strings_from_file

def extract_text(html):
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()

def get_request(witch:int, client_info:str):
    if not client_info.startswith("Имя"):
        text_otklika =  extract_text(client_info)
    else:
        text_otklika = client_info
    strings_dict = read_strings_from_file()
    answer1 = strings_dict['answer1']
    predistoriya = strings_dict['predistoriya']
    pro_clienta = strings_dict['pro_clienta']
    instrukcii = strings_dict['instrukcii']
    request = f"{predistoriya} ''' {answer1} ''' {pro_clienta} ''' {text_otklika} ''' {instrukcii}"
    return request

def get_request1(witch:int, client_info:str, midle_text:str = None):
    if not client_info.startswith("Имя"):
        text_otklika =  extract_text(client_info)
    else:
        text_otklika = client_info
    strings_dict = read_strings_from_file()
    
    answer2 = strings_dict['answer2']
    predistoriya2 = strings_dict['predistoriya2']
    pro_clienta2 = strings_dict['pro_clienta2']
    instrukcii2 = strings_dict['instrukcii2']
    if not midle_text:
        midle_text = strings_dict['midle_text']
    request = f"{predistoriya2} ''' {answer2} ''' {pro_clienta2} ''' {text_otklika} ''' {instrukcii2} Продолжением того что ты напишешь будет: {midle_text}. Самое это продолжение не пиши."
    return request

def get_request2(witch:int, client_info:str, midle_text:str = None):
    if not client_info.startswith("Имя"):
        text_otklika =  extract_text(client_info)
    else:
        text_otklika = client_info
    strings_dict = read_strings_from_file()
    answer3 = strings_dict['answer3']
    predistoriya3 = strings_dict['predistoriya3']
    pro_clienta3 = strings_dict['pro_clienta2']
    instrukcii3 = strings_dict['instrukcii2']
    if not midle_text:
        midle_text = strings_dict['midle_text']
    request = f"{predistoriya3} ''' {answer3} ''' {pro_clienta3} ''' {text_otklika} ''' {instrukcii3} '''  Начало быо такое: {midle_text}. Самое это начало не пиши."
    return request