from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_buttons_currency():
    keyboard = InlineKeyboardMarkup()
    for currency in ['RUB', 'USD', 'EUR']:
        key = InlineKeyboardButton(text=currency, callback_data=currency)
        keyboard.add(key)
    return keyboard
