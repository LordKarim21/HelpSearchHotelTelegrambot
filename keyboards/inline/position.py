from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_buttons_position():
    keyboard = InlineKeyboardMarkup()
    text = ['Да', 'Нет']
    callback_data = ['True', 'False']
    for index in range(len(text)):
        key = InlineKeyboardButton(text=text[index], callback_data=callback_data[index], block=True)
        keyboard.add(key)
    return keyboard
