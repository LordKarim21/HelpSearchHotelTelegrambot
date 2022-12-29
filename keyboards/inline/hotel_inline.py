from typing import Dict
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_hotel(hotel_data: Dict):
    keyboard = InlineKeyboardMarkup()
    for city in hotel_data['sr'][:5]:

        key = InlineKeyboardButton(
                text=city['regionNames']['fullName'],
                callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
        )
        keyboard.add(key)
    return keyboard
