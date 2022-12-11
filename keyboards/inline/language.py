from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_buttons_language():
    keyboard = InlineKeyboardMarkup()
    text = ['русский', 'english']
    callback_data = ["en_EN", "ru_RU"]
    for index in range(len(text)):
        key = InlineKeyboardButton(text=text[index], callback_data=callback_data[index])
        keyboard.add(key)
    return keyboard
