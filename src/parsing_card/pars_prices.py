"""
Модуль pars_prices.py содержит функции для извлечения цен из строк, содержащихся в объявлениях.
"""

from re import findall

def parse_upper(upper_str) -> tuple:
    """
    Функция parse_upper принимает строку в качестве входных данных и возвращает кортеж из двух целых
    чисел, представляющих верхние границы диапазона, извлеченных из входной строки.
    
    :param upper_str: Параметр «upper_str» — это строка, представляющая верхний диапазон. Он может
    содержать числа, разделенные пробелами или другими символами
    :return: Функция parse_upper возвращает кортеж из двух целых чисел.
    """
    # Если входная строка None или 'None'
    if upper_str is None or upper_str.lower() == 'none':
        return (0, 0)

    # Заменяем неразрывные пробелы на обычные
    upper_str = upper_str.replace('\u202f', '')

    # Проверяем, есть ли в строке цифры
    if not any(char.isdigit() for char in upper_str):
        return (0, 0)

    # Извлекаем цифры
    nums = findall(r'\d+', upper_str)
    if len(nums) == 1:
        return (int(nums[0]), int(nums[0]))
    elif len(nums) == 2:
        return (int(nums[0]), int(nums[1]))

    # Если в строке было больше 2 чисел, возвращаем первые два
    return (int(nums[0]), int(nums[1]))

def parse_prices(lower_str, upper_str) -> tuple:
    """
    Функция parse_prices принимает две строки, представляющие нижний и верхний пределы цен, и возвращает
    кортеж проанализированных значений нижней и верхней цен.
    
    :param lower_str: Строка, представляющая нижний предел цены. Это может быть одно из трех значений:
    «Нет», «от» (что означает «от») или «до» (что означает «до»)
    :param upper_str: Параметр «upper_str» — это строка, представляющая верхний предел ценового
    диапазона
    :return: Функция parse_prices возвращает кортеж, содержащий два значения.
    """
    upper = parse_upper(upper_str)
    if lower_str is None:
        return upper[0], upper[1]
    elif lower_str.lower() == 'от':
        return upper[0], 100000
    elif lower_str.lower() == 'до':
        return 0, upper[1]
    else:
        return upper[0], upper[1]

def test_parse_params():
    """
    Функция test_parse_params() тестирует функцию parse_prices() с различными вариантами ввода и
    проверяет, соответствует ли вывод ожидаемым значениям.
    """
    test_cases = [
        # Обычный диапазон
        ('от', '2500 ₽', 2500, 100000),
        ('None', '1700–3200 ₽', 1700, 3200),
        ('до', '2900 ₽', 0, 2900),
        ('None', '500–2500 ₽', 500, 2500),
        ('None', 'None', 0, 100000),
        # Диапазон с открытой верхней границей
        ('до', '5000 ₽', 0, 5000),
        ('None', '5000 ₽', 5000, 5000),
        # Диапазон с открытой нижней границей
        ('от', '5000 ₽', 5000, 100000),
        ('None', 'от', 0, 100000),
        # Диапазон с указанием только нижней границы
        ('от', 'None', 0, 100000),
        ('от', '1000 ₽', 1000, 100000),
        # Диапазон с указанием только верхней границы
        ('None', '1000 ₽', 1000, 1000),
        ('до', '1000 ₽', 0, 1000),
        # Другие входные значения
        (None, None, 0, 100000),
        ('от', '0 ₽', 0, 100000)
    ]
    for lower, upper, expected_lower, expected_upper in test_cases:
        #print (f"Тестируем {lower} и {upper}")
        result_lower, result_upper = parse_prices(lower, upper)
        assert result_lower == expected_lower, f"Ошибка при обработке {lower} и {upper}: ожидаемое значение нижней границы {expected_lower}, полученное значение {result_lower}"
        assert result_upper == expected_upper, f"Ошибка при обработке {lower} и {upper}: ожидаемое значение верхней границы {expected_upper}, полученное значение {result_upper}"
    #print("Все тесты пройдены успешно!")

#test_parse_params()

def test_parse_upper():
    """
    Функция test_parse_upper() тестирует функцию parse_upper(), предоставляя различные тестовые примеры
    и сравнивая ожидаемый результат с фактическим результатом.
    """
    test_cases = [
        # Обычный диапазон
        ('2500 ₽', 2500, 2500),
        ('1700–3200 ₽', 1700, 3200),
        ('2900 ₽', 2900, 2900),
        ('500–2500 ₽', 500, 2500),
        ('5000 ₽', 5000, 5000),
        ('от', 0, 0),
        # Диапазон с указанием только нижней границы
        ('None', 0, 0),
        ('1000 ₽', 1000, 1000),
        # Другие входные значения
        (None, 0, 0),
        ('0 ₽', 0, 0),
        ('', 0, 0),
        ('до', 0, 0),
        ('ываываы', 0, 0),
        ('sdfwefwef', 0, 0),
        ('0 ₽', 0, 0),
    ]
    for  upper, expected_lower, expected_upper in test_cases:
        #print (f"Тестируем  {upper}")
        result_lower, result_upper = parse_upper(upper)
        assert result_lower == expected_lower, f"Ошибка при обработке  {upper}: ожидаемое значение нижней границы {expected_lower}, полученное значение {result_lower}"
        assert result_upper == expected_upper, f"Ошибка при обработке  {upper}: ожидаемое значение верхней границы {expected_upper}, полученное значение {result_upper}"
    #print("Все тесты пройдены успешно!")

#test_parse_upper()