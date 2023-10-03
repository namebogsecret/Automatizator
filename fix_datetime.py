from dateutil import parser

def fix_datetime_function(wrong_datetime):
    try:
        # Попытаться преобразовать строку в объект datetime
        dt = parser.parse(wrong_datetime)
        # Преобразовать объект datetime обратно в строку в нужном формате
        fixed_datetime = dt.strftime('%Y-%m-%d %H:%M:%S')
        return fixed_datetime
    except Exception as e:
        print(f"Could not parse datetime {wrong_datetime}: {e}")
        return None

# Пример использования
wrong_datetime = "2021-21-09 12::30:25"  # Неверный формат
fixed_datetime = fix_datetime_function(wrong_datetime)
if fixed_datetime:
    print(f"Fixed datetime is {fixed_datetime}")
else:
    print("Could not fix datetime")
