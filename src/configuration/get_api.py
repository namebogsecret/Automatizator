from dotenv import load_dotenv
import os
load_dotenv()
def get_api():
    """Get the API key from the api.txt file"""
    api = os.getenv("gpt_api")
    return api
    # content = None
    # with open('src/configuration/api.txt', 'r', encoding='utf-8') as file:
    #     content = file.read()
    # return content