from typing import Dict
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_keyboard_city(city_data: Dict):
    keyboard = InlineKeyboardMarkup()
    for city in city_data['sr']:
        if city['type'].lower() in ['city']:
            key = InlineKeyboardButton(
                text=city['regionNames']['fullName'],
                # callback_data='Id:{}, coordinates:{}'.format(city['essId']['sourceId'], city['coordinates'])
                callback_data='Id:{}'.format(city['essId']['sourceId'])
            )
            keyboard.add(key)
    return keyboard
