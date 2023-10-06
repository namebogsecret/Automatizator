#from constants.texts import answer1
#from constants.dict import dict_otklik
from src.configuration.read_strings_from_file import read_strings_from_file

def chouse_avtootklik_text(variant: str, params: dict={}) -> str: #variant = ili from dict_otklik 'dict', ili sam text 'text'
    if variant == 'dict':
        otklik_text = "first_avtootklik"
        if otklik_text != None:
            return otklik_text
    if variant == 'text':
        strings_dict = read_strings_from_file()
        answer1 = strings_dict['answer1']
        return str(answer1)
    return ""
    