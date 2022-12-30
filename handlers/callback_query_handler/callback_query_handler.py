from typing import Dict
from telebot.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar
from utils.date.get_date import run_calendar
from database.user_data import set_region_id, get_arrival_date, set_arrival_date, get_departure_date, \
    set_departure_date, get_command
from utils.hotel_num.hotel_num import get_hotel_num
from loader import bot
from handlers.basic_handlers.best_deal import get_max_price
from utils.photo.question_amount_photo import get_photo_amount
from utils.response.get_response import response_hotels


@bot.callback_query_handler(func=lambda call: "Id" in call.data)
def get_city(call: CallbackQuery) -> None:
    region_id = call.data.split(":")[1]
    set_region_id(call.from_user.id, int(region_id))
    bot.send_message(call.message.chat.id, 'Выберите дату приезда')
    run_calendar(call.message)
    bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def get_data(call: CallbackQuery):
    LSTEP_RU: Dict[str: str] = {"y": "год", "m": "месяц", "d": "день"}
    result, key, step = DetailedTelegramCalendar(locale="ru").process(call.data)
    if not result and key:
        bot.edit_message_text(f"Выберите {LSTEP_RU[step]}",
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        if get_arrival_date(call.from_user.id) == "None" and get_departure_date(call.from_user.id) == "None":
            bot.edit_message_text(f"Вы выбрали дату приезда: {result}", call.message.chat.id, call.message.message_id)
            bot.send_message(call.message.chat.id, 'Выберите дату уезда')
            set_arrival_date(call.from_user.id, str(result))
            run_calendar(call.message)
        elif get_departure_date(call.from_user.id) == "None" and get_arrival_date(call.from_user.id) != "None":
            bot.edit_message_text(f"Вы выбрали дату уезда: {result}", call.message.chat.id, call.message.message_id)
            set_departure_date(call.from_user.id, str(result))
            if get_command(call.from_user.id) != "bestdeal":
                msg = bot.send_message(call.from_user.id, "Спасибо, записал. Теперь введи число отелей")
                bot.register_next_step_handler(msg, get_hotel_num)
            else:
                msg = bot.send_message(chat_id=call.message.chat.id, text='Введите вашу высокую цену')
                bot.register_next_step_handler(msg, get_max_price)
        bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: call.data in ["True", "False"])
def get_position_photo(call: CallbackQuery) -> None:
    if call.data == "True":
        msg = bot.send_message(call.from_user.id, "Введите количество фотографий")
        bot.register_next_step_handler(msg, get_photo_amount)
    else:
        response_hotels(call.message)
    bot.answer_callback_query(callback_query_id=call.id)
