# Функция для проверки, отображается ли элемент на странице
def element_is_displayed(element):
    return element.value_of_css_property('display') != 'none'
