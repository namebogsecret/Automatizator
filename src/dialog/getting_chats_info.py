from otklik.is_it_on_the_page import WebScraper

def geting_chats_info(driver):

    open_url = "https://profi.ru/backoffice/r.php?filter=open" # открытые заказы
    in_progress_url = "https://profi.ru/backoffice/r.php?filter=in_progress" # в работе
    vipolneni_url = "https://profi.ru/backoffice/r.php?filter=executed" # заказ выполнен
    archive_url = "https://profi.ru/backoffice/r.php?filter=archive" # не договорились
    #div type = INITIAL
    w1 = WebScraper(driver, "dict_otklik")
    # Find element by class ending with 'faTkYO'
    chat_elements = w1.is_it_on_the_page("chat_element", only_one=False)
    if chat_elements:
        for chat_element in chat_elements:
            #get id
            chat_id = chat_element.get_attribute("id")
            print(chat_id)
            w2 = WebScraper(driver, "dict_otklik")
            top_string = w2.is_it_on_the_page("top_string")
            if top_string:
                print(top_string.text)
            galki = w2.is_it_on_the_page("galki")
            if galki:
                transform_style = galki.get_attribute("style")
                if "scale(0);" in transform_style:
                    print("SVG element  is hidden.")
                else:
                    print("SVG element  is visible.")
                    svg = galki.find_element_by_tag_name("svg")
                    paths = svg.find_elements(By.TAG_NAME, 'path')
    
                    for i, path in enumerate(paths):
                        stroke_color = path.get_attribute('stroke')
                        stroke_dashoffset = path.get_attribute('stroke-dashoffset')

                        if stroke_color == "#0075ff" and stroke_dashoffset == "0":
                            print("SVG element  is of the first type.")
                        elif stroke_color == "#7e8287" and stroke_dashoffset == "10":
                            print("SVG element  is of the second type.")
