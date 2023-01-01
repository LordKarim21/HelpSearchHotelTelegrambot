from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_url(property_id):
    markup = InlineKeyboardMarkup()
    text = "Перейти"
    url = "https://www.hotels.com/h{}.Hotel-Information".format(property_id)
    btn = InlineKeyboardButton(text=text, url=url)
    markup.add(btn)
    return markup
