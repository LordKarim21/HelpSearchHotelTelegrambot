from calendar import month_name, monthcalendar
from datetime import datetime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_calendar(year=None, month=None):
    keyboard = InlineKeyboardMarkup()
    now = datetime.now()
    year = now.year if year is None else year
    month = now.month if month is None else month

    data_ignore = ";".join(['IGNORE', str(year), str(month), str(0)])
    # First row - Month and Year
    row = InlineKeyboardButton(text=month_name[month] + " " + str(year), callback_data=data_ignore)
    keyboard.add(row)
    # Second row - Week Days
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row = InlineKeyboardButton(text=day, callback_data=data_ignore)
    keyboard.add(row)

    my_calendar = monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row = InlineKeyboardButton(text=" ", callback_data=data_ignore)
            else:
                data_day = ";".join(['DAY', str(year), str(month), str(day)])
                row = InlineKeyboardButton(text=str(day), callback_data=data_day)
        keyboard.add(row)
    return keyboard
