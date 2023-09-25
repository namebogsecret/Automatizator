import asyncio
from telegram import Bot
#from telegram import request
from configuration.read_strings_from_file import read_strings_from_file

class TelegramBot:
    def __init__(self, chat_id, numer_of_bot: int = 1):#, token1: str = '6146861942:AAG2_2aaHSZG3p1SyX1C77OrdRZsD6y0frU', token2 = "5600318053:AAFKhNIcFNTr35URWLkArWMAlAx5DH8r1VA"):
        strings_dict = read_strings_from_file()
        t_api1 = strings_dict['t_api1']
        t_api2 = strings_dict['t_api2']
        if numer_of_bot == 1:
            self.token = t_api1
        else:
            self.token = t_api2
        self.chat_id = chat_id

    async def send_message_sync(self, message: str, del_then = True):
        
        self.bot = Bot(token=self.token)
        sent_message = await self.bot.send_message(chat_id=self.chat_id, text=message)
        if del_then:
            self.last_message_id = sent_message.message_id
        del self.bot

    async def delete_message_sync(self, mesage_id):
        self.bot = Bot(token=self.token)
        await self.bot.delete_message(chat_id=self.chat_id, message_id=mesage_id)
        del self.last_message_id
        del self.bot

    def send_message(self, message: str, del_then = True):
        asyncio.run(self.send_message_sync(message, del_then))
    
    def delete_message(self, mesage_id):
        asyncio.run(self.delete_message_sync(mesage_id))

    def delete_last_message(self):
        if hasattr(self, 'last_message_id'):
            self.delete_message(self.last_message_id)



#класс для работы с ботами
class TelegramBots:
    def __init__(self, number_of_bots: int = 1):
        self.bots = {"kate": TelegramBot(416177154, number_of_bots),
                     "iphone": TelegramBot(2125928660, number_of_bots),
                     "moscow": TelegramBot(1696774734, number_of_bots),
                     "developer": TelegramBot(585870101, number_of_bots)}
    def rassilka(self, message: str, del_then = True):
        for bot in self.bots.values():
            bot.delete_last_message()
        for bot in self.bots.values():
            bot.send_message(message, del_then)
    
    def to_all_mine(self, message: str, del_then = True):
        self.bots["iphone"].delete_last_message()
        self.bots["moscow"].delete_last_message()
        self.bots["developer"].delete_last_message()
        self.bots["iphone"].send_message(message, del_then)
        self.bots["moscow"].send_message(message, del_then)
        self.bots["developer"].send_message(message, del_then)
    
    def to_android(self, message: str, del_then = True):
        self.bots["moscow"].delete_last_message()
        self.bots["developer"].delete_last_message()
        self.bots["moscow"].send_message(message, del_then)
        self.bots["developer"].send_message(message, del_then)
        
    def to_developer(self, message: str, del_then = True):
        self.bots["developer"].delete_last_message()
        self.bots["developer"].send_message(message, del_then)


async def telegram_message(message: str, chat_id: int):
    strings_dicts = read_strings_from_file()
    t_api1 = strings_dicts['t_api1']
    bot = Bot(token=t_api1)
    # замените на ID пользователя, которому вы хотите отправить сообщение
    sent_message = await bot.send_message(chat_id=chat_id, text=message)
    return sent_message.message_id
    
def maessage_to_kate(message: str):
    strings_dicts = read_strings_from_file()
    kate_chat_id = int(strings_dicts['kate_chat_id'])
    asyncio.run(telegram_message(message,kate_chat_id))

def maessage_to_iphone(message: str):
    strings_dicts = read_strings_from_file()
    iphone_chat_id = int(strings_dicts['iphone_chat_id'])
    asyncio.run(telegram_message(message,iphone_chat_id))
    
def maessage_to_moscow(message: str):
    strings_dicts = read_strings_from_file()
    moscow_chat_id = int(strings_dicts['moscow_chat_id'])
    asyncio.run(telegram_message(message,moscow_chat_id))
    
def maessage_to_developer(message: str):
    strings_dicts = read_strings_from_file()
    DEVELOPER_CHAT_ID = int(strings_dicts['DEVELOPER_CHAT_ID'])
    asyncio.run(telegram_message(message,DEVELOPER_CHAT_ID))


def rassilka(message: str):
    maessage_to_kate(message)
    maessage_to_iphone(message)
    maessage_to_moscow(message)
    maessage_to_developer(message)

def to_all_mine(message: str):
    maessage_to_developer(message)
    maessage_to_iphone(message)
    maessage_to_moscow(message)
    
def to_android(message: str):
    maessage_to_developer(message)
    maessage_to_moscow(message)
    
async def delete_message(chat_to_delete_id, mesage_id):
    strings_dicts = read_strings_from_file()
    t_api1 = strings_dicts['t_api1']
    bot = Bot(token=t_api1)
    await bot.delete_message(chat_id=chat_to_delete_id, message_id=mesage_id)