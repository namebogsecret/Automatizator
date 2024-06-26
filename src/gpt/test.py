# {
#     "name": "application_writer_do_not_whant_distant",
#     "description": "Основные инструкции: пиши без особой фантазии, нужно что бы запрос был релятивен информации клиента,\nесли нужны дополнительные языки знаю только английский и русский.\n'С уважением' в конце добавлять не нужно.\nВ именах ошибаться нельзя и менять или сокращать их тоже нельзя. Пиши как человек.\nМое конечное сообщение будет иметь такую структуру:\n///\n'privetstvie'\n'средняя неизменная часть сообщения'\n'distant_advertasing' (если необходимо и предусмотрено)\n'proshanie'\n'стоимость урока'\n'naputstvie'\n///\nnaputstvie я могу и не включать, поэтому и без него все должно быть понятно.\nПиши от моего имени. Меня зовут Подлевских Владимир,\nя один из лучших репетиторов по физике и математике.\nЯ из Москвы, занимаюсь только дистанционно.",
#     "parameters": {
#       "type": "object",
#       "properties": {
#         "privetstvie": {
#           "type": "string",
#           "description": "Твоя задача переписать это приветствие, сделать его персонализированным, что бы он подходил для клиента с полученной информацией.\nДалее представлен текст приветственной части моего стандартного ответа на заяявку клиента (меня зовут Владимир Подлевских из Москвы занимаюсь только дистанционно):\n///Здравствуйте, Мария! С удовольствием помогу вашему сыну Максиму со сдачей ОГЭ по физике.///"
#         },
#         "distant_advertasing": {
#           "type": "string",
#           "description": "Если клиент написал категорично, что не хочет дистанционно, и занятия должны быть только очно, то ты должен написать почему дистанционный формат даже в чем-то удобнее очного, а благодаря новым технолигям (например Zoom) качество занятий такое же."
#         },
#         "proshanie": {
#           "type": "string",
#           "description": "Далее представлен текст заключительной части моего стандартного ответа на заяявку клиента:\n///На первом занятии мы пройдемся по темам математики и определим уровень знаний Максима, что позволит составить маршрут дальнейшей подготовки и проконтролировать прогресс.\nНадеюсь на сотрудничество и готов ответить на возникающие вопросы. Удачи вам и Максиму в подготовке к поступлению!///\nТебе нужно персонализировать эту заключительную часть в соответствии с информацией о потенциальном клиенте, которую ты получил."
#         },
#         "naputstvie": {
#           "type": "string",
#           "description": "Эта фраза, которая будет в конце сообщения, Она должна быть короткой, соответствовать действительности и тому что ты написал выше, и должна привлекать внимание потенциального клиента и вызывать желание прочитать все сообщение.\nНе больше 7 слов.\nПримеры:\n'Опытный репетитор с МГУ — 20 лет стажа.'\n'Первое занятие: полный анализ уровня.'"
#         }
#       },
#       "required": ["privetstvie", "distant_advertising", "proshanie", "naputstvie"]
#     }
#   },

# {
#     "name": "application_writer_whant_distant",
#     "description": "Основные инструкции: пиши без особой фантазии, нужно что бы запрос был релятивен информации клиента,\nесли нужны дополнительные языки знаю только английский и русский.\n'С уважением' в конце добавлять не нужно.\nВ именах ошибаться нельзя и менять или сокращать их тоже нельзя. Пиши как человек.\nМое конечное сообщение будет иметь такую структуру:\n///\n'privetstvie'\n'средняя неизменная часть сообщения'\n'distant_advertasing' (если необходимо и предусмотрено)\n'proshanie'\n'стоимость урока'\n'naputstvie'\n///\nnaputstvie я могу и не включать, поэтому и без него все должно быть понятно.\nПиши от моего имени. Меня зовут Подлевских Владимир,\nя один из лучших репетиторов по физике и математике.\nЯ из Москвы, занимаюсь только дистанционно.",
#     "parameters": {
#       "type": "object",
#       "properties": {
#         "privetstvie": {
#           "type": "string",
#           "description": "Твоя задача переписать это приветствие, сделать его персонализированным, что бы он подходил для клиента с полученной информацией.\nДалее представлен текст приветственной части моего стандартного ответа на заяявку клиента (меня зовут Владимир Подлевских из Москвы занимаюсь только дистанционно):\n///Здравствуйте, Мария! С удовольствием помогу вашему сыну Максиму со сдачей ОГЭ по физике.///"
#         },
#         "distant_advertasing": {
#           "type": "string",
#           "description": "Если клиент написал категорично, что не хочет дистанционно, и занятия должны быть только очно, то ты должен написать почему дистанционный формат даже в чем-то удобнее очного, а благодаря новым технолигям (например Zoom) качество занятий такое же."
#         },
#         "proshanie": {
#           "type": "string",
#           "description": "Далее представлен текст заключительной части моего стандартного ответа на заяявку клиента:\n///На первом занятии мы пройдемся по темам математики и определим уровень знаний Максима, что позволит составить маршрут дальнейшей подготовки и проконтролировать прогресс.\nНадеюсь на сотрудничество и готов ответить на возникающие вопросы. Удачи вам и Максиму в подготовке к поступлению!///\nТебе нужно персонализировать эту заключительную часть в соответствии с информацией о потенциальном клиенте, которую ты получил."
#         },
#         "naputstvie": {
#           "type": "string",
#           "description": "Эта фраза, которая будет в конце сообщения, Она должна быть короткой, соответствовать действительности и тому что ты написал выше, и должна привлекать внимание потенциального клиента и вызывать желание прочитать все сообщение.\nНе больше 7 слов.\nПримеры:\n'Опытный репетитор с МГУ — 20 лет стажа.'\n'Первое занятие: полный анализ уровня.'"
#         }
#     },
#     "required": [ "privetstvie", "proshanie", "naputstvie"]
#     }
# }

print("""({"privetstvie": "\u0417\u0434\u0440\u0430\u0432\u0441\u0442\u0432\u0443\u0439\u0442\u0435, \u0410\u043d\u0430\u0441\u0442\u0430\u0441\u0438\u044f! \u041e\u0447\u0435\u043d\u044c \u0440\u0430\u0434 \u0432\u043e\u0437\u043c\u043e\u0436\u043d\u043e\u0441\u0442\u0438 \u043f\u043e\u043c\u043e\u0447\u044c \u042e\u043b\u0435 \u0443\u043b\u0443\u0447\u0448\u0438\u0442\u044c \u0443\u0441\u043f\u0435\u0432\u0430\u0435\u043c\u043e\u0441\u0442\u044c \u043f\u043e \u0433\u0435\u043e\u043c\u0435\u0442\u0440\u0438\u0438.", "distant_advertasing": "\u0423\u0431\u0435\u0434\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u043f\u0440\u043e\u0448\u0443 \u0440\u0430\u0441\u0441\u043c\u043e\u0442\u0440\u0435\u0442\u044c \u0432\u043e\u0437\u043c\u043e\u0436\u043d\u043e\u0441\u0442\u044c \u0434\u0438\u0441\u0442\u0430\u043d\u0446\u0438\u043e\u043d\u043d\u044b\u0445 \u0437\u0430\u043d\u044f\u0442\u0438\u0439. \u0411\u043b\u0430\u0433\u043e\u0434\u0430\u0440\u044f \u043f\u0435\u0440\u0435\u0434\u043e\u0432\u044b\u043c \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u044f\u043c, \u043a\u0430\u043a Zoom, \u0437\u0430\u043d\u044f\u0442\u0438\u044f \u043e\u043d\u043b\u0430\u0439\u043d \u043c\u0430\u043a\u0441\u0438\u043c\u0430\u043b\u044c\u043d\u043e \u044d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u044b \u0438 \u043f\u043e\u0437\u0432\u043e\u043b\u044f\u044e\u0442 \u044d\u043a\u043e\u043d\u043e\u043c\u0438\u0442\u044c \u0432\u0440\u0435\u043c\u044f \u043d\u0430 \u0434\u043e\u0440\u043e\u0433\u0443, \u0430 \u0442\u0430\u043a\u0436\u0435 \u043e\u0431\u0435\u0441\u043f\u0435\u0447\u0438\u0432\u0430\u044e\u0442 \u043a\u043e\u043c\u0444\u043e\u0440\u0442 \u0438 \u0431\u0435\u0437\u043e\u043f\u0430\u0441\u043d\u043e\u0441\u0442\u044c \u0432\u0430\u0448\u0435\u0433\u043e \u0440\u0435\u0431\u0435\u043d\u043a\u0430. \u041a \u0442\u043e\u043c\u0443 \u0436\u0435, \u0432 \u043d\u044b\u043d\u0435\u0448\u043d\u0435\u043c \u0432\u0435\u043a\u0435 \u0446\u0438\u0444\u0440\u043e\u0432\u044b\u0445 \u0442\u0435\u0445\u043d\u043e\u043b\u043e\u0433\u0438\u0439, \u043e\u0441\u0432\u043e\u0435\u043d\u0438\u0435 \u0434\u0438\u0441\u0442\u0430\u043d\u0446\u0438\u043e\u043d\u043d\u043e\u0439 \u0440\u0430\u0431\u043e\u0442\u044b \u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f \u043d\u0435\u043e\u0442\u044a\u0435\u043c\u043b\u0435\u043c\u044b\u043c \u043d\u0430\u0432\u044b\u043a\u043e\u043c.", "proshanie": "\u041d\u0430\u0447\u043d\u0435\u043c \u0441 \u0430\u043d\u0430\u043b\u0438\u0437\u0430 \u0443\u0440\u043e\u0432\u043d\u044f \u0437\u043d\u0430\u043d\u0438\u0439 \u042e\u043b\u0438 \u0438 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0430\u0435\u043c \u043f\u0435\u0440\u0441\u043e\u043d\u0430\u043b\u0438\u0437\u0438\u0440\u043e\u0432\u0430\u043d\u043d\u0443\u044e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0443 \u0434\u043b\u044f \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f \u0435\u0435 \u0443\u0441\u043f\u0435\u0432\u0430\u0435\u043c\u043e\u0441\u0442\u0438. \u042f \u0433\u043e\u0442\u043e\u0432 \u043e\u0442\u0432\u0435\u0442\u0438\u0442\u044c \u043d\u0430 \u043b\u044e\u0431\u044b\u0435 \u0432\u0430\u0448\u0438 \u0432\u043e\u043f\u0440\u043e\u0441\u044b \u0438 \u043d\u0430\u0434\u0435\u044e\u0441\u044c \u043d\u0430 \u043d\u0430\u0448\u0435 \u0441\u043e\u0442\u0440\u0443\u0434\u043d\u0438\u0447\u0435\u0441\u0442\u0432\u043e. \u0416\u0435\u043b\u0430\u044e \u042e\u043b\u0435 \u0443\u0441\u043f\u0435\u0445\u043e\u0432 \u0432 \u0443\u0447\u0435\u0431\u0435!", "naputstvie": "\u042d\u0444\u0444\u0435\u043a\u0442\u0438\u0432\u043d\u044b\u0435 \u043e\u043d\u043b\u0430\u0439\u043d-\u0443\u0440\u043e\u043a\u0438 \u043f\u043e \u0433\u0435\u043e\u043c\u0435\u0442\u0440\u0438\u0438."})""")