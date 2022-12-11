from datetime import datetime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def _get_years():
    year = datetime.now().year
    years_list = [i for i in range(year, year + 3)]
    keyboard = InlineKeyboardMarkup()
    for year in years_list:
        key = InlineKeyboardButton(text=str(year), callback_data=str(year)+"years")
        keyboard.add(key)
    return keyboard
