from otklik.is_it_on_the_page import WebScraper
from otklik.get_page import get_page
from time import sleep
from random import random

def geting_chats_info(driver):
    print("geting_chats_info")
    open_url = "https://profi.ru/backoffice/r.php?filter=open" # открытые заказы
    in_progress_url = "https://profi.ru/backoffice/r.php?filter=in_progress" # в работе
    vipolneni_url = "https://profi.ru/backoffice/r.php?filter=executed" # заказ выполнен
    archive_url = "https://profi.ru/backoffice/r.php?filter=archive" # не договорились
    #div type = INITIAL
    if not get_page(driver, open_url):
        print("Не удалось открыть страницу")
        return False
    sleep(3 + random())
    w1 = WebScraper(driver, "dict_chat_status")
    # Find element by class ending with 'faTkYO'
    chat_elements = w1.is_it_on_the_page("chat_element", only_one=False)
    if chat_elements:
        print("chat_elements")
        for chat_element in chat_elements:
            print("chat_element")
            #get id
            chat_id = chat_element.get_attribute("id")
            print(chat_id)
            w2 = WebScraper(driver, "dict_chat_status")
            top_string = w2.is_it_on_the_page("top_string")
            if top_string:
                print(top_string.text)
            galki = w2.is_it_on_the_page("galki")
            if galki:
                print("galki")
                transform_style = galki.get_attribute("style")
                if "scale(0);" in transform_style:
                    print("SVG element  is hidden.")
                else:
                    print("SVG element  is visible.")
                    w3 = WebScraper(galki, "dict_chat_status")
                    svg = w3.is_it_on_the_page("svg")
                    if svg:
                        print("svg")
                        w4 = WebScraper(svg, "dict_chat_status")
                        paths = w4.is_it_on_the_page("path", only_one=False)
                        if paths:
                            print("paths")
                            for i, path in enumerate(paths):
                                print("path")
                                stroke_color = path.get_attribute('stroke')
                                stroke_dashoffset = path.get_attribute('stroke-dashoffset')

                                if stroke_color == "#0075ff" and stroke_dashoffset == "0":
                                    print("SVG element  is of the first type.")
                                elif stroke_color == "#7e8287" and stroke_dashoffset == "10":
                                    print("SVG element  is of the second type.")
    return True
