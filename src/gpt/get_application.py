
import json
from os import getenv

from icecream import ic
import openai
from dotenv import load_dotenv
from functools import lru_cache

@lru_cache(maxsize=20)
def get_application(user_info: str, middle_text: str, whant_distant: bool = False, temperature = 0.1) -> json:
    user_info = json.loads(user_info)
    load_dotenv()

    openai.api_key = getenv("gpt_api")

    model = "gpt-4" # "gpt-4", #"gpt-3.5-turbo","gpt-4-1106-preview"

    # temperature = 0.1

    description = """
    Основные инструкции: пиши без особой фантазии, нужно что бы запрос был релятивен информации клиента,
    если нужны дополнительные языки знаю только английский и русский.
    'С уважением' в конце добавлять не нужно.
    В именах ошибаться нельзя и менять или сокращать их тоже нельзя. Пиши как человек.
    Мое конечное сообщение будет иметь такую структуру:
    ///
    'privetstvie'
    'средняя неизменная часть сообщения'
    'distant_advertasing' (если необходимо и предусмотрено)
    'proshanie'
    'стоимость урока'
    'naputstvie'
    ///
    naputstvie я могу и не включать, поэтому и без него все должно быть понятно.
    Пиши от моего имени. Меня зовут Подлевских Владимир,
    я один из лучших репетиторов по физике и математике.
    Я из Москвы, занимаюсь только дистанционно.
    Пиши от первого единственного числа.
    """
    
    privetstvie_description = """
    Твоя задача переписать это приветствие, сделать его персонализированным, что бы он подходил для клиента с полученной информацией.
    Далее представлен текст приветственной части моего стандартного ответа на заяявку клиента (меня зовут Владимир Подлевских из Москвы занимаюсь только дистанционно):
    ///Здравствуйте, Мария! С удовольствием помогу вашему сыну Максиму со сдачей ОГЭ по физике.///          
    """

    proshanie_description = """
    Далее представлен текст заключительной части моего стандартного ответа на заяявку клиента:
    ///На первом занятии мы пройдемся по темам математики и определим уровень знаний Максима,
    что позволит составить маршрут дальнейшей подготовки и проконтролировать прогресс.
    Надеюсь на сотрудничество и готов ответить на возникающие вопросы. Удачи вам и Максиму в подготовке к поступлению!///
    Тебе нужно персонализировать эту заключительную часть в соответствии с информацией о потенциальном клиенте, которую ты получил.
    """

    distant_advertising = """
    Если клиент написал категорично, что не хочет дистанционно, 
    и занятия должны быть только очно, 
    то ты должен написать почему дистанционный формат даже в чем-то удобнее очного,
    а благодаря новым технолигям (например Zoom) качество занятий такое же.
    """

    naputstvie = """
    Эта фраза, которая В самом начале сообщения, ее увидят до прочтения всего сообщения,
    Она должна быть короткой, соответствовать действительности и тому что ты написал выше,
    и должна привлекать внимание потенциального клиента и вызывать желание прочитать все сообщение.
    Так же она должна быть персонализирована.
    Не больше 14 слов.
    Примеры (прямо их не используй, но можешь взять за основу):
    'Егор, вам нужен опытный репетитор из МГУ — с 20 летним стажем.'
    'Мария, на первом занятие мы сделаем полный анализ уровня.'
    """

    if not whant_distant:
        functions = [
            {
                "name": "application_writer_do_not_whant_distant",
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "privetstvie": {
                            "type": "string",
                            "description": privetstvie_description
                        },
                        "distant_advertasing": {
                            "type": "string",
                            "description": distant_advertising
                        },
                        "proshanie": {
                            "type": "string",
                            "description": proshanie_description
                        },
                        "naputstvie": {
                            "type": "string",
                            "description": naputstvie
                        },
                    },
                    "required": [ "privetstvie", "distant_advertising", "proshanie", "naputstvie"]
                },
            },
        ]
    else:
        functions = [
            {
                "name": "application_writer_whant_distant",
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "privetstvie": {
                            "type": "string",
                            "description": privetstvie_description,
                        },
                        "proshanie": {
                            "type": "string",
                            "description": proshanie_description
                        },
                        "naputstvie": {
                            "type": "string",
                            "description": naputstvie
                        },
                    },
                    "required": [ "privetstvie", "proshanie", "naputstvie"]
                },
            },
        ]
    messages = []
    messages.append({"role": "system", "content": f"""
                     Ты топовый репетитор по физике и математике, который может подготовить любого к поступлению в МГУ или другой топовый вуз,
                        а так же помчь с успеваемостью или подготовиться к контрольной или экзамену.
                     Ты получил информацию о потенциальном ученике и его родителе.
                     Ты должен написать клиенту очень уважительно, обращаясь по имени.
                     Врать нельзя.
                     Обещать то, чего я не могу нельзя.
                     'средняя неизменная часть сообщения' = {middle_text}
                     В описаниях функции даны последующие указания и примеры."""})
    messages.append({"role": "user", "content": f"""Составь мне сообщение для потенциального ученика или его родителя, которое будет подходить для клиента с такой информацией: ///
                     {user_info}///"""})
    # Шаг 2: Сформировать запрос к модели

    # Шаг 3: Вызвать модель
    try:
        response = openai.ChatCompletion.create(
            model=model, # "gpt-4", #"gpt-3.5-turbo",
            messages=messages,
            functions=functions,
            function_call="auto", #{"name": "client_details_parser"},
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

    #subject = function_call_args.get("subject", None)
    resived_privetstvie = function_call_args.get("privetstvie", None)
    resived_distant_advertasing = function_call_args.get("distant_advertasing", None)
    resived_proshanie = function_call_args.get("proshanie", None)
    resived_naputstvie = function_call_args.get("naputstvie", None)

    json_data = {
        "privetstvie": resived_privetstvie,
        "middle_text": middle_text,
        "distant_advertasing": resived_distant_advertasing if resived_distant_advertasing else "",
        "proshanie": resived_proshanie,
        "naputstvie": resived_naputstvie
    }
    # ic(json_data)
    # print(f" json_data: {json_data}")
    return json_data


if __name__ == "__main__":
    all_text1 = """{'client_name': 'Анастасия',
                              'description': 'Повышение успеваемости',
                              'exam': '',
                              'location': 'микрорайон Климовск, Подольск, Московская область, Россия, '
                                          'Заводская улица, 19',
                              'on_what_plaсe_is_my_responce': '1',
                              'other': '',
                              'preferences': '«Просьба знакомиться внимательно перед отправкой сообщений. '
                                             'Только очно! Рассмотрю Подольск, Климовск.»',
                              'remote': False,
                              'student_data': {'grade': '8 класс', 'name': 'Юля'},
                              'subject': 'Геометрия',
                              'time_until_exam': ''}"""
    all_text = """{
    "client_name": "Анастасия",
    "description": "Повышение успеваемости",
    "exam": "",
    "location": "микрорайон Климовск, Подольск, Московская область, Россия, Заводская улица, 19",
    "on_what_plaсe_is_my_responce": "1",
    "other": "",
    "preferences": "«Просьба знакомиться внимательно перед отправкой сообщений. Только очно! Рассмотрю Подольск, Климовск.»",
    "remote": false,
    "student_data": {"grade": "8 класс", "name": "Юля"},
    "subject": "Геометрия",
    "time_until_exam": ""
}"""
    middle_text = """Мой опыт подготовки школьников к поступлению составляет более 20 лет. Важно отметить, что начальный уровень знаний не имеет значения. Я готов помочь школьникам с любым уровнем подготовки, от нулевого до продвинутого. 

Применяю разработанную мной авторскую методику. Самый важный элемент - домашнее задание, которое составляет 70% от общего результата. 

Я хочу поделиться с вами примерами прогресса, которые мои ученики демонстрируют за разные периоды времени: 

- За 2 года ученик даже с нулевого уровня подготовки может поступить в любой вуз при условии желания и исполнения домашних заданий. 
- За 1 год ученик может на 30-60 баллов поднять результат ЕГЭ. 
- За полгода - поднять уровень на 20-40 баллов. 
- За 3 месяца - на 10-20 баллов.

В этом году все занятия проводятся дистанционно. Цена за занятие составляет 5000 р. за 60 минут или 6000 р. за 90 минут. Возможна оплата как за одно занятие, так и за месяц вперед. 

Важно отметить, что мои ученики успешно поступают в различные вузы, включая МГУ, МГТУ, ВШЭ, РГУ нефти и газа им. Губкина и многие другие. 
"""
    user_data = json.loads(all_text)
    ic(get_application(all_text,middle_text, whant_distant=bool(user_data.get("remote", False))))