from typing import Dict
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_city(city_data: Dict):
    keyboard = InlineKeyboardMarkup()
    for city in city_data['sr']:
        key = InlineKeyboardButton(
            text=city['regionNames']['fullName'],
            callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
        )
        keyboard.add(key)
    return keyboard
