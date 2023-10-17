"""
Модуль для получения информации о чатах с сайта profi.ru.
Использует веб-скрапинг для извлечения необходимых данных.
"""

from time import sleep
from random import random
import csv

from otklik.is_it_on_the_page import WebScraper
from otklik.get_page import get_page
from webdriver.scroll import scroll_down

def geting_chats_info(driver):
    """
    Функция для получения информации о чатах с сайта profi.ru.

    Параметры:
    driver (WebDriver): драйвер браузера для веб-скрапинга.

    Возвращает:
    bool: Возвращает True, если операция прошла успешно, иначе False.
    """
    
    # URLs для различных фильтров заказов
    open_url = "https://profi.ru/backoffice/r.php?filter=open"
    in_progress_url = "https://profi.ru/backoffice/r.php?filter=in_progress"
    vipolneni_url = "https://profi.ru/backoffice/r.php?filter=executed"
    archive_url = "https://profi.ru/backoffice/r.php?filter=archive"
    
    # Открываем архивные заказы
    if not get_page(driver, open_url):
        print("Не удалось открыть страницу")
        return False
    
    # Ожидание загрузки страницы
    sleep(10 + random())
    scroll_down(driver, 500)
    input("Нажмите Enter, когда загрузится страница")
    # Инициализация WebScraper для данной страницы
    w1 = WebScraper(driver, "dict_chat_status")
    
    # Поиск всех чатов на странице
    chat_elements = w1.is_it_on_the_page("chat_element", only_one=False)
    statuses = []

    if chat_elements:
        for chat_element in chat_elements:
            status = "не читал"
            #print("!!!!!!!!!!! не читал? !!!!!!!!!!!")
            # Получение ID чата
            chat_id = chat_element.get_attribute("id")
            #print (chat_id)
            # Новый WebScraper для каждого чата
            w2 = WebScraper(chat_element, "dict_chat_status")
            
            # Поиск верхнего текста в чате
            top_string = w2.is_it_on_the_page("top_string")
            if top_string:
                top_string = top_string.text
            else:
                top_string = ""
            
            # Поиск элемента "galki" на странице
            galki = w2.is_it_on_the_page("galki")
            
            if galki:
                #print(galki.is_displayed())
                # Проверка видимости элемента "galki"
                transform_style = galki.get_attribute("style")
                #print(transform_style)
                if "scale(0);" in transform_style:
                    #print("SVG element  is hidden.")
                    #print ("!!!!!!!!!!! ответил? !!!!!!!!!!!")
                    status = "ответил"
                else:
                    #print("SVG element  is visible.")
                    
                    # Новый WebScraper для элемента "galki"
                    w3 = WebScraper(galki, "dict_chat_status")
                    svg = w3.is_it_on_the_page("svg")
                    
                    if svg:
                        # Новый WebScraper для элемента "svg"
                        w4 = WebScraper(svg, "dict_chat_status")
                        
                        # Поиск всех путей в элементе "svg"
                        paths = w4.is_it_on_the_page("path", only_one=False)
                        if paths:
                            #print(len(paths))
                            for i, path in enumerate(paths):
                                # Получение атрибутов для каждого пути
                                """print(path)
                                outer_html = path.get_attribute('outerHTML')
                                print(outer_html)"""
                                stroke_color = path.get_attribute('stroke')
                                stroke_dashoffset = path.get_attribute('stroke-dashoffset')

                                # Определение типа SVG элемента
                                if stroke_color == "#0075ff" and stroke_dashoffset == "0":
                                    #print("SVG element  is of the first type.")
                                    #print("!!!!!!!!!!! Посмотрел? !!!!!!!!!!!")
                                    status = "посмотрел"
                                    """elif stroke_color == "#7e8287" and stroke_dashoffset == "10":
                                        #print("SVG element  is of the second type.")
                                        sleep(0.01)
                                    else:
                                        sleep(0.01)"""
                                    #print("SVG element  is of the third type.")
                                    #print("!!!!!!!!!!! 4")
                                
                        #print("!!!!!!! 1")
                    #print("!!!!!!! 2")
                
            """else:
                #print("No SVG element.")
                sleep(0.01)"""
            #print(f"{chat_id} Status: {status}. Top string: {top_string}")  # Выводим текущий статус
            statuses.append((chat_id, status, top_string))
    with open('open_url_statuses.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Статус', 'Сообщение'])  # Заголовок CSV
        csvwriter.writerows(statuses)
    #print(f"Status: {status}")
    return True
