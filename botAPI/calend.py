"""
Base methods for calendar keyboard creation and processing.
"""

from datetime import datetime
import calendar
import json

from telebot import types


def _get_years():
    year = datetime.now().year
    years_list = [i for i in range(year, year + 3)]
    keyboard = types.InlineKeyboardMarkup()
    for year in years_list:
        key = types.InlineKeyboardButton(text=str(year), callback_data=year)
        keyboard.add(key)
    return keyboard


def _valid_year(year: str):
    if year.startswith('3'):
        return False
    else:
        try:
            datetime.strptime(year, '%Y')
            return True
        except (ValueError, TypeError):
            return False


def _get_month(data):
    month_list = [i for i in range(1, 13)] * 2
    month = datetime.now().month
    year = data
    months_list = [calendar.month_name[i] for i in month_list[month-1: month + 11]]
    keyboard = types.InlineKeyboardMarkup()
    for month in months_list[:4]:
        key = types.InlineKeyboardButton(text=month, callback_data=" ".join((month, year)))
        keyboard.add(key)
    return keyboard


def _valid_month(value: str):
    month = value.split(" ")[0]
    try:
        month = str(month)
        datetime.strptime(month, '%B')
        return True
    except (ValueError, TypeError):
        return False


def _valid_date(date: str):
    try:
        noun, year, month, day = date.split(';')
        if "IGNORE" == noun:
            return False
        datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None, month=None):
    now = datetime.now()
    year = now.year if year is None else year
    month = now.month if month is None else month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    markup = {"inline_keyboard": []}
    # First row - Month and Year
    row = [{"text": calendar.month_name[month] + " " + str(year), "callback_data": data_ignore}]
    markup["inline_keyboard"].append(row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append({"text": day, "callback_data": data_ignore})
    markup["inline_keyboard"].append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append({"text": " ", "callback_data": data_ignore})
            else:
                row.append({"text": "{}".format(day), "callback_data": create_callback_data("DAY", year, month, day)})
        markup["inline_keyboard"].append(row)
    return json.dumps(markup)
