
from os import getenv
import dotenv

dotenv.load_dotenv()

def get_api():
    api = getenv('gpt_api')
    return api
