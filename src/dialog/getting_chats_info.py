from otklik.is_it_on_the_page import WebScraper

def geting_chats_info(driver):

    open_url = "https://profi.ru/backoffice/r.php?filter=open" # открытые заказы
    in_progress_url = "https://profi.ru/backoffice/r.php?filter=in_progress" # в работе
    vipolneni_url = "https://profi.ru/backoffice/r.php?filter=executed" # заказ выполнен
    archive_url = "https://profi.ru/backoffice/r.php?filter=archive" # не договорились
    #div type = INITIAL
    w1 = WebScraper(driver, "dict_otklik")
    # Find element by class ending with 'faTkYO'
    if w1.is_it_on_the_page("chat_page"):
        