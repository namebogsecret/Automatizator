#from parsing_card.pars_prices import parse_prices

def has_right_price(lower, upper, price):
    """Проверяет, попадает ли цена в диапазон"""
    if lower == 0 and upper == 100000:
        return True
    if lower <= price <= upper:
        if upper == 100000:
            if lower >= price * 0.7:
                return True
            else:
                return False
        return True
    if lower == upper and price <= lower*1.3:
        return True
    return False