from telebot.types import Message, CallbackQuery
from loader import bot
from keyboards.inline.currency import get_inline_buttons_currency
from keyboards.inline.language import get_inline_buttons_language


@bot.message_handler(commands=['settings'])
def command_settings(message: Message):
    question = 'Установить валюту по умолчанию:'
    keyboard = get_inline_buttons_currency()
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    question = 'Установить язык по умолчанию:'
    keyboard = get_inline_buttons_language()
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['RUB', 'USD', 'EUR'])
def change_cur(call: CallbackQuery) -> None:
    """Установка валюты пользователем"""
    with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
        data['currency'] = call.data
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.callback_query_handler(func=lambda call: call.data in ["en_EN", "ru_RU"])
def change_lang(call: CallbackQuery) -> None:
    """Установка языка пользователем"""
    with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
        data['language'] = call.data
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

