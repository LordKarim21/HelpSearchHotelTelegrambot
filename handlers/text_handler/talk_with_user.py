from telebot.types import Message
from loader import bot


@bot.message_handler(content_types=['text'])
def start_message_user(message: Message):
    text = "Для начало введите команду /info_travel"
    bot.send_message(message.from_user.id, text)
