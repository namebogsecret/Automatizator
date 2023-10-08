#/crc/otklik/last_cards_chek.py
from logging import getLogger
from src.otklik.load_card_html import load_card_html
from src.database.update_students_data import update_students_data
from src.log_scripts.set_logger import set_logger
#from database.temp_removed import is_temp_removed
#from database.temp_removed import remove_temp_removed
from src.database.temp_removed import add_temp_removed
from selenium.webdriver import Chrome
from src.database.table_handle import Database_Simple_Table
from datetime import datetime
from src.parsing_card.has_right_price import has_right_price
from src.parsing_card.pars_prices import parse_prices
#from constants.constants import my_price
from src.configuration.read_strings_from_file import read_strings_from_file
from src.database.for_last_card_check import get_student, get_urls, get_applications



logger = getLogger(__name__)
logger = set_logger(logger)

def last_cards_check(number_of_cards: int, sql, driver: Chrome, cards_parsed, otklikov: int, vakansiy: int, deleted: int, errors: int, nepodhodit: int, banned: int, limited: int):
    ban_tabel = Database_Simple_Table(sql, "banned")
    strings_dict = read_strings_from_file()
    _my_price2 = strings_dict['my_price_2'] # to do
    my_price = int(strings_dict['my_price'])
    limit_tabel = Database_Simple_Table(sql, "limit_exided")
    temp_removed = Database_Simple_Table(sql, "Students_temp_removed")
    # если сейчас с 01:30 до 02:00 ночи, то удаляем все записи из таблицы лимитов
    if datetime.now() > datetime(datetime.now().year, datetime.now().month, datetime.now().day, 1, 30) and datetime.now() < datetime(datetime.now().year, datetime.now().month, datetime.now().day, 2, 0):
        limit_tabel.delete_all_from_table()
    logger.info("Проверка последних %s карточек", number_of_cards)
    #cursor = sql.cursor()
    for card in cards_parsed:
        #cursor.execute("SELECT id FROM studentsdata WHERE id = ?", (card['id'],))
        if get_student(sql, card['id']) is None:
            if card['ot_do'] is None:
                lower_price, upper_price = parse_prices(None, card['price'])
            else:
                lower_price, upper_price = parse_prices(card['ot_do'], card['price'])
            if not has_right_price(lower_price, upper_price, my_price):
                logger.info("Карточка %s не подходит по цене", card['id'])
                #nepodhodit += 1
                continue
            if card['url'] is None:
                logger.error("Карточка %s не имеет ссылки", card)
                errors += 1
                continue
            if temp_removed.check_if_exists(card['id']):
                logger.info("Карточка %s находится в базе отложенных", card['id'])
                temp_removed.delete_from_table(card['id'])
                #remove_temp_removed(card['id'], sql)
            if ban_tabel.check_if_exists(card['id']):
                logger.info("Карточка %s находится в базе забаненных", card['id'])
                continue
            if limit_tabel.check_if_exists(card['id']):
                logger.info("Карточка %s находится в базе лимитов", card['id'])
                continue
            logger.info("Проверка карточки %s", card['id'])
            result, html, html_choose, html_otklik_param, all_text, ban, limit = load_card_html(card['url'], driver, sql)
            if result == "Vakans":
                logger.info("Заполняем вакансию %s", card['id'])
                vakansiy += 1
                update_students_data(card['url'], sql, "Vakans", html, html_choose, html_otklik_param, all_text)
            elif result == "Allready":
                logger.info("Уже откликнулись %s", card['id'])
                update_students_data(card['url'], sql, "Allready", html, html_choose, html_otklik_param, all_text)
                otklikov += 1
            elif result == "Error":
                logger.info("Ошибка при заполнении %s", card['id'])
                errors += 1
            elif result == "Nepodhodit":
                update_students_data(card['url'], sql, "NePodhodit", html, html_choose, html_otklik_param, all_text)
                nepodhodit += 1
            elif result == "Sent":
                logger.info("Добавляем откликнулись %s", card['id'])
                update_students_data(card['url'], sql, "Allready", html, html_choose, html_otklik_param, all_text)
                otklikov += 1
            elif result == "Deleted":
                logger.info("Карточка %s удалена (слишком долго обрабатывали)", card['id'])
                add_temp_removed(card['id'], sql, html)
                deleted += 1
            elif result == "Ban":
                if not ban_tabel.check_if_exists(card['id']):
                    banned += 1
                    ban_tabel.add_to_table(card['id'])
            elif result == "Limit":
                if not limit_tabel.check_if_exists(card['id']):
                    limited += 1
                    limit_tabel.add_to_table(card['id'])
            else:
                logger.error("Неизвестный результат %s", card['id'])
                errors += 1
        else:
            logger.info("Карточка %s уже проверена", card['id'])
    """try:
        cursor.execute("SELECT url FROM Applications ORDER BY timestamp_last DESC LIMIT ?", (number_of_cards,))
    except Exception as e:"""
    urls = get_urls(sql, number_of_cards)
    if urls is None:
        logger.error("Не удалось выполнить запрос к базе данных.")
        errors += 1
        return otklikov, vakansiy, deleted, errors, nepodhodit, banned, limited
    """cursor.execute("SELECT url, ot_do, price FROM Applications WHERE NOT EXISTS (SELECT 1 FROM StudentsData WHERE StudentsData.id = Applications.id) ORDER BY timestamp_last DESC LIMIT ?", (number_of_cards,))
    rows = cursor.fetchall()"""
    applications = get_applications(sql, number_of_cards)
    if len(applications) == 0:
        logger.info("Нет карточек для добавления в базу данных")
        errors += 1
        return otklikov, vakansiy, deleted, errors, nepodhodit, banned, limited
    else:
        logger.info("Карточки для добавления:")
        for row in applications:
            start_index = row[0].find('o=') + 2
            end_index = row[0].find('&', start_index)
            student_id = row[0][start_index:end_index]
            logger.info(row[0])
            if row[1] is None:
                if row[2] is None:
                    lower_price, upper_price = parse_prices(None, None)
                else:
                    lower_price, upper_price = parse_prices(None, row[2])
            else:
                if row[2] is None:
                    lower_price, upper_price = parse_prices(row[1], None)
                else:
                    lower_price, upper_price = parse_prices(row[1], row[2])
            if not has_right_price(lower_price, upper_price, my_price):
                logger.info("Карточка %s не подходит по цене", student_id)
                #nepodhodit += 1
                continue
            if temp_removed.check_if_exists(student_id):
                logger.info("Карточка %s находится в базе отложенных", student_id)
                continue
            if ban_tabel.check_if_exists(student_id):
                logger.info("Карточка %s находится в базе забаненных", student_id)
                continue
            if limit_tabel.check_if_exists(student_id):
                logger.info("Карточка %s находится в базе лимитов", student_id)
                continue
            result, html, html_choose, html_otklik_param, all_text, ban, limit = load_card_html(row[0], driver, sql)
            if result == "Vakans":
                vakansiy += 1
                logger.info("Заполняем вакансию %s", student_id)
                update_students_data(row[0], sql, "Vakans", html, html_choose, html_otklik_param, all_text)
            elif result == "Allready":
                otklikov += 1
                logger.info("Уже откликнулись %s", student_id)
                update_students_data(row[0], sql, "Allready", html, html_choose, html_otklik_param, all_text)
            elif result == "Error":
                errors += 1
                logger.info("Ошибка см лог load_card_html %s", student_id)
            elif result == "Nepodhodit":
                update_students_data(row[0], sql, "NePodhodit", html, html_choose, html_otklik_param, all_text)
                logger.info("Не подходит %s", student_id)
                nepodhodit += 1
            elif result == "Sent":
                otklikov += 1
                logger.info("Добавляем откликнулись %s", student_id)
                update_students_data(row[0], sql, "Allready", html, html_choose, html_otklik_param, all_text)
            elif result == "Deleted":
                deleted += 1
                logger.info("Карточка %s уже удалена", student_id)
                temp_removed.add_to_table(student_id)
                #add_temp_removed(student_id, sql, html)
            elif result == "Ban":
                if not ban_tabel.check_if_exists(student_id):
                    ban_tabel.add_to_table(student_id)
                    banned += 1
            elif result == "Limit":
                if not limit_tabel.check_if_exists(student_id):
                    limit_tabel.add_to_table(student_id)
                    limited += 1
            else:
                errors += 1
                logger.error("Неизвестный результат %s", student_id)
        return otklikov, vakansiy, deleted, errors, nepodhodit, banned, limited