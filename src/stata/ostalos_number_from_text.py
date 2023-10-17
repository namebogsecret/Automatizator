
from re import search as re_search

def extract_number_before_today(text):
    """
    Извлекает число, предшествующее слову "сегодня" в тексте.
    
    Parameters:
    text (str): Входной текст.

    Returns:
    int or None: Возвращает число если найдено, иначе None.
    """
    # Используем регулярное выражение для поиска числа перед словом "сегодня"
    match = re_search(r'(\d+)\s*сегодня', text)
    if match:
        return int(match.group(1))
    else:
        return None

if __name__ == "__main__":
    # Пример использования
    text = "50 в день, ещё 0 сегодня"
    result = extract_number_before_today(text)
    print(f"Число перед словом 'сегодня': {result}")