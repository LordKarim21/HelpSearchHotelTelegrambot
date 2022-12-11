from datetime import datetime
import calendar
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_month(year=None):
    month_list = [i for i in range(1, 13)] * 2
    now = datetime.now()
    year = now.year if year is None else year
    month = now.month
    months_list = [calendar.month_name[i] for i in month_list[month-1: month + 11]]
    keyboard = InlineKeyboardMarkup()
    for month in months_list[:4]:
        key = InlineKeyboardButton(text=month, callback_data=" ".join((month, year)))
        keyboard.add(key)
    return keyboard
