
import json
from os import getenv

from icecream import ic
import openai
from dotenv import load_dotenv
from gpt.get_application import get_application
from time import time

def get_user_data(all_text:str) -> json:
    load_dotenv()

    openai.api_key = getenv("gpt_api")

    model = "gpt-3.5-turbo" # "gpt-4", #"gpt-3.5-turbo",

    temperature = 0.1

    functions = [
            {
                "name": "client_details_parser",
                "description": f"Из полученной строки необходимо извлечь все возможные данные, если какого-то пункта нет, оставляй пустую строку, если встречается что-то что не учтено в данных категриях - пиши в категорию ‘other’",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string", "description": "Предмет, по которому требуется помощь."},
                        #"price": {"type": "string", "description": "Стоимость услуги в час."},
                        "description": {"type": "string", "description": "Описание услуги."},
                        "student": {
                            "type": "object",
                            "description": "Информация об ученике.",
                            "properties": {
                                "name": {"type": "string", "description": "Имя ученика."},
                                "grade": {"type": "string", "description": "Класс ученика."}
                            },
                            "required": ["name", "grade"]
                        },
                        "location": {"type": "string", "description": "Местоположение ученика."},
                        #"availability": {"type": "string", "description": "Доступность по времени."},
                        "preferences": {"type": "string", "description": "Особые пожелания клиента."},
                        #"commission": {"type": "string", "description": "Комиссия за услугу."},
                        "other":{"type": "string", "description": "Все что не вошло в остальные параметры"},
                        "exam": {
                            "type": "string",
                            "description": "Экзамен, который предстоит сдать."
                        },
                        "remote": {
                            "type": "boolean",
                            #"enum": ["celsius", "fahrenheit"],
                            "description": "Готовы заниматься дистанционно, или хотят только очно. Если готовы дистанционно, то True, если только очно, то False."
                        },
                        "time_until_exam": {
                            "type": "string",
                            "description": "Время, оставшееся до экзамена."
                        },
                        # "order_details": {
                        #     "type": "object",
                        #     "description": "Детали заказа.",
                        #     "properties": {
                        #         "number": {"type": "string", "description": "Номер заказа."},
                        #         "posted": {"type": "string", "description": "Дата и время размещения заказа."},
                        #         "updated": {"type": "string", "description": "Дата и время последнего обновления заказа."}
                        #     },
                        #     "required": ["number", "posted", "updated"]
                        # },
                        "client": {
                            "type": "object",
                            "description": "Информация об клиенте.",
                            "properties": {
                                "name": {"type": "string", "description": "Имя агента."},
                                # "status": {"type": "string", "description": "Статус онлайн агента."},
                                # "joined": {"type": "string", "description": "Дата присоединения агента к сервису."},
                                # "phone_verified": {"type": "boolean", "description": "Был ли подтвержден номер телефона агента."}
                            },
                            "required": ["name"]#, "status", "joined", "phone_verified"]
                        },
                        #"feedback": {"type": "boolean", "description": "Наличие отзывов от специалистов."},
                        "response_rank": {"type": "string", "description": "Рейтинг отклика на заказ."}
                    },
                    "required": [ "subject", "description", "student", "location", "preferences", "client", "response_rank", "other", "exam", "remote", "time_until_exam"]
                    #["subject", "price", "description", "student", "location", "availability", "preferences", "commission", "order_details", "agent", "feedback", "response_rank", "other"]
                }, 
            },
        ]

    # Шаг 2: Сформировать запрос к модели
    messages = [{"role": "user", "content": all_text}]

    # Шаг 3: Вызвать модель
    try:
        response = openai.ChatCompletion.create(
            model=model, # "gpt-4", #"gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call={"name": "client_details_parser"},
            temperature=temperature
        )
        #ic(response)
    except Exception as e:
        #ic(f"Exception: {e}")
        return None

    # Шаг 4: Обработать результат
    try:
        response_content = response["choices"][0]["message"]
    except Exception as e:
        #ic(f"Exception: {e}")
        return None
    #print(f" response_content: {response_content}")
    function_call_args = response_content.get("function_call", {}).get("arguments", None)
    #print(f" function_call_args: {function_call_args}")
    if function_call_args is None:
        return None
    # print(f" function_call_args: {function_call_args}")

    function_call_args = json.loads(function_call_args)
    #ic(function_call_args)
    subject = function_call_args.get("subject", None)
    #price = function_call_args.get("price", None)
    description = function_call_args.get("description", None)
    student = function_call_args.get("student", None)
    location = function_call_args.get("location", None)
    #availability = function_call_args.get("availability", None)
    preferences = function_call_args.get("preferences", None)
    #commission = function_call_args.get("commission", None)
    #order_details = function_call_args.get("order_details", None)
    client = function_call_args.get("client", None)
    client_name = client.get("name", None)
    #feedback = function_call_args.get("feedback", None)
    on_what_plaсe_is_my_responce = function_call_args.get("response_rank", None)
    other = function_call_args.get("other", None)
    exam = function_call_args.get("exam", None)
    remote = function_call_args.get("remote", None)
    time_until_exam = function_call_args.get("time_until_exam", None)

    json_data = {
        "subject": subject,
        "description": description,
        "student_data": student,
        "location": location,
        "preferences": preferences,
        "client_name": client_name,
        "on_what_plaсe_is_my_responce": on_what_plaсe_is_my_responce,
        "other": other,
        "exam": exam,
        "remote": remote,
        "time_until_exam": time_until_exam
    }
    # ic(json_data)
    # print(f" json_data: {json_data}")
    return json_data

if __name__ == "__main__":
    start_time = time()
    all_text = """Геометрия
до 1400 руб./ч
Описание
Повышение успеваемости
Ученик
Юля, 8 класс.
У ученика
Показать карту
микрорайон Климовск, Подольск, Московская область, Россия, Заводская улица, 19
Климовск
Когда
пн, вт, ср, чт, пт (с 15:00 до 20:00)
Пожелания
«Просьба знакомиться внимательно перед отправкой сообщений. Только очно! Рассмотрю Подольск, Климовск.»
Комиссия
1900 руб.
Детали заказа
№ 61635535
Заказ оставлен вчера в 07:45
Обновлен вчера в 18:35
А
Анастасия
В сети 1 час назад
На Профис 20 октября 2019
Подтвердиланомер
Отзывов от специалистов пока нет
Вы откликнулись на этот заказ. Ваш отклик 1-й по рейтингу."""
    middle_text = """
    Мой опыт подготовки школьников к поступлению составляет более 20 лет. Важно отметить, что начальный уровень знаний не имеет значения. Я готов помочь школьникам с любым уровнем подготовки, от нулевого до продвинутого. 

Применяю разработанную мной авторскую методику. Самый важный элемент - домашнее задание, которое составляет 70% от общего результата. 

Я хочу поделиться с вами примерами прогресса, которые мои ученики демонстрируют за разные периоды времени: 

- За 2 года ученик даже с нулевого уровня подготовки может поступить в любой вуз при условии желания и исполнения домашних заданий. 
- За 1 год ученик может на 30-60 баллов поднять результат ЕГЭ. 
- За полгода - поднять уровень на 20-40 баллов. 
- За 3 месяца - на 10-20 баллов.

В этом году все занятия проводятся дистанционно. Цена за занятие составляет 5000 р. за 60 минут или 6000 р. за 90 минут. Возможна оплата как за одно занятие, так и за месяц вперед. 

Важно отметить, что мои ученики успешно поступают в различные вузы, включая МГУ, МГТУ, ВШЭ, РГУ нефти и газа им. Губкина и многие другие. 
"""
    user_data = get_user_data(all_text)
    ic(user_data)
    application = get_application(user_data, middle_text, whant_distant=bool(user_data.get("remote", False)), temperature=0.9)
    all_time = time() - start_time
    ic(all_time)
    ic(application)
    # json_data = {
    #     "privetstvie": resived_privetstvie,
    #     "middle_text": middle_text,
    #     "distant_advertasing": resived_distant_advertasing if resived_distant_advertasing else "",
    #     "proshanie": resived_proshanie,
    #     "naputstvie": resived_naputstvie
    # }
    privetstvie = application.get("privetstvie", None)
    ic(privetstvie)
    distant_advertasing = application.get("distant_advertasing", None)
    ic(distant_advertasing)
    proshanie = application.get("proshanie", None)
    ic(proshanie)
    naputstvie = application.get("naputstvie", None)
    ic(naputstvie)

    print(f"""{privetstvie}
{middle_text}
{distant_advertasing} {proshanie}
{naputstvie}""")
    ic("end")