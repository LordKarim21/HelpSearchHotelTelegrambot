from typing import Dict
from telebot.types import Message
from telegram_bot_calendar import DetailedTelegramCalendar
from loader import bot


def run_calendar(message: Message):
    LSTEP_RU: Dict[str: str] = {"y": "год", "m": "месяц", "d": "день"}
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(message.chat.id,
                     f"Выберите {LSTEP_RU[step]}",
                     reply_markup=calendar)

