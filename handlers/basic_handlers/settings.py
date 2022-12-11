from telebot.types import Message
from loader import bot
from keyboards.inline.currency import get_inline_buttons_currency


@bot.message_handler(commands=['settings'])
def command_settings(message: Message):
    question = 'Установить валюту по умолчанию:'
    keyboard = get_inline_buttons_currency()
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
