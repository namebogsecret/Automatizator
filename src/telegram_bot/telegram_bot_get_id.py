#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import html
import json
import logging
import traceback
from telegram import ForceReply, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from telegram import __version__ as TG_VER
import ast
from src.configuration.read_strings_from_file import read_strings_from_file

strings_dict = read_strings_from_file()
DEVELOPER_CHAT_ID = strings_dict['DEVELOPER_CHAT_ID']
kate_chat_id = strings_dict['kate_chat_id']
iphone_chat_id = strings_dict['iphone_chat_id']
moscow_chat_id = strings_dict['moscow_chat_id']

"""DEVELOPER_CHAT_ID = 585870101
kate_chat_id = 416177154
iphone_chat_id = 2125928660
moscow_chat_id = 1696774734"""
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )

def contains_dangerous_code(text: str) -> bool:
    """Check if the text contains dangerous Python code."""
    try:
        ast.parse(text)
        return False
    except SyntaxError:
        return True

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    channel_chat_created = update.message.channel_chat_created
    chat = update.message.chat
    date = update.message.date
    delete_chat_photo = update.message.delete_chat_photo
    entities = update.message.entities
    from_user = update.message.from_user
    group_chat_created = update.message.group_chat_created
    message_id = update.message.message_id
    reply_to_message = update.message.reply_to_message
    supergroup_chat_created = update.message.supergroup_chat_created
    text = update.message.text
    update_id = update.update_id
    # Подкатегории внутри chat
    chat_id = chat.id
    chat_type = chat.type
    chat_first_name = chat.first_name
    chat_last_name = chat.last_name

    # Подкатегории внутри from_user
    user_id = from_user.id
    user_first_name = from_user.first_name
    user_last_name = from_user.last_name
    user_is_bot = from_user.is_bot
    user_language_code = from_user.language_code

    # Подкатегории внутри reply_to_message
    #reply_message_id = reply_to_message.message_id
    #reply_message_text = reply_to_message.text

    # Подкатегории внутри entities
    entity_type = entities[0].type
    entity_offset = entities[0].offset
    entity_length = entities[0].length
    
    """print("All parameters are printed below:")
    print("channel_chat_created: ", channel_chat_created)
    print("chat_id: ", chat_id)
    print("chat_type: ", chat_type)
    print("chat_first_name: ", chat_first_name)
    print("chat_last_name: ", chat_last_name)
    print("date: ", date)
    print("delete_chat_photo: ", delete_chat_photo)
    print("entity_type: ", entity_type)
    print("entity_offset: ", entity_offset)
    print("entity_length: ", entity_length)
    print("from_user_id: ", user_id)
    print("from_user_first_name: ", user_first_name)
    print("from_user_last_name: ", user_last_name)
    print("from_user_is_bot: ", user_is_bot)
    print("from_user_language_code: ", user_language_code)
    print("group_chat_created: ", group_chat_created)
    print("message_id: ", message_id)
    #print("reply_message_id: ", reply_message_id)
    #print("reply_message_text: ", reply_message_text)
    print("supergroup_chat_created: ", supergroup_chat_created)
    print("text: ", text)
    print("update_id: ", update_id)"""
    
    
    user = update.effective_user
    
    chat_id = update.effective_chat.id
    
    
    #print (f"User {user.mention_html()} started the conversation. User_id is {user.id} and chat_id is {chat_id}")
    await update.message.reply_html(f"User All your are:\nUser_id is {user.id}\nChat_id is {chat_id}\nChannel_chat_created is {channel_chat_created}\nChat_type is {chat_type}\nChat_first_name is {chat_first_name}\nChat_last_name is {chat_last_name}\nDate is {date}\nDelete_chat_photo is {delete_chat_photo}\nEntity_type is {entity_type}\nEntity_offset is {entity_offset}\nEntity_length is {entity_length}\nFrom_user_id is {user_id}\nFrom_user_first_name is {user_first_name}\nFrom_user_last_name is {user_last_name}\nFrom_user_is_bot is {user_is_bot}\nFrom_user_language_code is {user_language_code}\nGroup_chat_created is {group_chat_created}\nMessage_id is {message_id}\nSupergroup_chat_created is {supergroup_chat_created}\nText is {text}\nUpdate_id is {update_id}", reply_markup=ForceReply(selective=True))
    """await update.message.reply_html(
        rf"Hi {user.mention_html()}! Your user_id is {user.id} and chat_id is {chat_id}",
        reply_markup=ForceReply(selective=True),
    )"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your user_id is {user.id} and chat_id is {chat_id}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    # Проверяем наличие вредоносного кода
    if contains_dangerous_code(update.message.text):
        await update.message.reply_text("Пожалуйста, не отправляйте вредоносный код p в этот чат!")
        return
    
    message = update.message.text.lower()
    
    # Фильтруем сообщения на наличие нежелательных слов
    if "спам" in message or "реклама" in message:
        await update.message.reply_text("Пожалуйста, не спамьте в этом чате!")
        return

    # Проверяем наличие вредоносного кода
    if "<script>" in message:
        await update.message.reply_text("Пожалуйста, не отправляйте вредоносный код j в этот чат!")
        return

    await update.message.reply_text(f"Your user_id is {user.id} and chat_id is {chat_id}. You said: {message}")

def my_telegram_bot() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    strings_dict = read_strings_from_file()
    t_api2 = strings_dict["t_api2"]
    application = Application.builder().token("t_api2").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    # ...and the error handler
    application.add_error_handler(error_handler)
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    my_telegram_bot()