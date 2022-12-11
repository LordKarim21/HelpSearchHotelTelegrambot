import calendar
from datetime import datetime
from typing import Optional

from keyboards.inline.calendar import create_calendar
from telebot.types import Message, CallbackQuery
from loader import bot

from keyboards.inline.years import _get_years
from keyboards.inline.months import get_month


def _valid_date(date: str):
    try:
        noun, year, month, day = date.split(';')
        if "IGNORE" == noun:
            return False
        datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def get_date(message: Message = None, call: CallbackQuery = None) -> Optional[str, None]:
    if message is not None:
        keyboard = _get_years()
        bot.send_message(message.chat.id, text='Спасибо, записал. Теперь уточните год', reply_markup=keyboard)
    elif call is not None:
        return call.data


@bot.callback_query_handler(func=lambda call: "years" in call.data)
def get_month(call: CallbackQuery) -> None:
    keyboard = get_month(call.data.split("years")[0])
    bot.send_message(call.message.chat.id, text='Уточните месяц', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: "-year" in call.data and "-month" in call.data)
def set_date(call: CallbackQuery) -> None:
    month_str, year_str = call.data.split(",")
    year = year_str.split("-")[0]
    month = month_str.split("-")[0]
    month_num = [num for num, name in enumerate(calendar.month_abbr) if name in month and num][0]
    markup = create_calendar(int(year), month_num)
    bot.send_message(call.message.chat.id, text='Уточните дату:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: _valid_date(call.data))
def call_date(call: CallbackQuery) -> None:
    get_date(call=call)
