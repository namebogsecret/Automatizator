from gpt.gpt import gpt

if __name__ == "__main__":
    
    html_about = 'математикаот 2800\xa0руб./чописаниеповышение успеваемостиученикандрей, 5 класс.адреспоказать картупроспект мира, 122алексеевскаяклиент может приехатьалексеевскаядетали заказа№ 55205075заказ оставлен 1 минуту назадуточнить деталиеекатерина сейчас в сетина профис 27 июля 2021подтвердиланомеротзывов от специалистов пока нетв этом заказе ваш отклик будет 1-м по рейтингу.'
    print (gpt(html_about, 111, gpt4 = True, temp = 1,timeout=120))