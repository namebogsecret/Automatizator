from otklik.is_it_on_the_page import WebScraper
from otklik.get_page import get_page
from time import sleep
from random import random

def getting_dialogs(driver):

    test_url = "https://profi.ru/backoffice/r.php?filter=executed&id=37793670"

    print('getting_dialogs')
    #div type = INITIAL
    if not get_page(driver, open_url):
        print("Не удалось открыть страницу")
        return False
    sleep(3 + random())
    
    # Извлекаем все блоки сообщений
    message_blocks = driver.find_elements_by_css_selector('.cwc_0Hlyhs')

    all_messages = []

    for block in message_blocks:
        # Проверка на системное сообщение
        if 'cwc_ML4iJU' in block.get_attribute('class'):
            system_msg = block.find_element_by_css_selector('.cwc_6jIf0j.cwc_BFgZYK').text
            time_element = block.find_element_by_css_selector('.cwc_KsECmV span').text
            all_messages.append(('Системное сообщение', time_element, system_msg))
        else:
            user_name_elements = block.find_elements_by_css_selector('.cwc_ztgn4q.cwc_p-nH8t')
            user_name = user_name_elements[0].text if user_name_elements else "Неизвестно"
            
            user_messages = block.find_elements_by_css_selector('.cwc_6jIf0j.cwc_BFgZYK')
            for msg in user_messages:
                time_element = msg.find_element_by_xpath('./following-sibling::div[@class="cwc_KsECmV"]//span')
                time = time_element.text if time_element else "Неизвестно"
                all_messages.append((user_name, time, msg.text))

    contacts = []
    contact_elements = driver.find_elements_by_css_selector('a[href^="tel:"]')
    for elem in contact_elements:
        contacts.append(elem.get_attribute('href').replace('tel:', ''))

    # Результат
    for name, time, text in all_messages:
        print(f"Имя: {name}, Время: {time}, Текст: {text}")

    print(f"Контакты: {contacts}")


