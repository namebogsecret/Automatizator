import requests
import json
from dotenv import load_dotenv
import os

class WebhookSender:
    def __init__(self):
        """
        Инициализирует класс, загружая переменные окружения и создавая сессию для запросов.
        """
        load_dotenv()
        self.webhook_url = os.getenv('hook_url')
        self.api_key = os.getenv('my_api')
        self.session = requests.Session()

    def send_webhook(self, data):
        """
        Отправляет POST-запрос на указанный URL с данными в формате JSON и API-ключом для аутентификации.

        :param data: Словарь с данными для отправки.
        """
        headers = {
            'Content-Type': 'application/json',
            'API-Key': self.api_key
        }
        try:
            response = self.session.post(self.webhook_url, data=json.dumps(data), headers=headers, verify=False)
            return response
        except requests.RequestException as e:
            return f"Произошла ошибка: {e}"

if __name__ == '__main__':
    # Использование класса
    sender = WebhookSender()

    # Данные для отправки
    data = {
        'service': 'Instagram',
        'event': 'New Post',
        'error': False,
        'message': 'Новая картинка опубликована'
    }

    # Отправка вебхука
    response = sender.send_webhook(data)
    print(f"Status Code: {response.status_code}, Response: {response.text}")
