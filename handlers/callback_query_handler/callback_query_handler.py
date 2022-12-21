from telebot.types import CallbackQuery
from config_data.contact_information import User
from handlers.basic_handlers.highprice import highprice
from handlers.basic_handlers.lowprice import lowprice
from handlers.basic_handlers.best_deal import bestdeal
from utils.hotel_num.hotel_num import get_hotel_num
from loader import bot
from handlers.basic_handlers.best_deal import get_max_price


@bot.callback_query_handler(func=lambda call: "Id" in call.data)
def get_city(call: CallbackQuery) -> None:
    msg = bot.send_message(call.from_user.id, "Спасибо, записал. Теперь введи число отелей")
    region_id = call.data.split(":")[1]
    print(region_id, call.chat_instance)
    data = User.get_data_with_user(call.from_user.id)
    data['city'] = call.message.text
    data['region_id'] = int(region_id)
    if data['command'] != "bestdeal":
        bot.register_next_step_handler(msg, get_hotel_num)
    else:
        bot.register_next_step_handler(msg, get_max_price)


@bot.callback_query_handler(func=lambda call: call.data in ["True", "False"])
def get_position_photo(call: CallbackQuery) -> None:
    bot.send_message(call.from_user.id, "Спасибо, записал. \nГотово")
    data = User.get_data_with_user(call.from_user.id)
    if call.data == "True":
        data['photos_uploaded']['status'] = True
        data['photos_uploaded']['number_of_photos'] = 10
        data["hotels_number_to_show"] = 10
    if data['command'] == "lowprice":
        bot.register_next_step_handler(call.message, lowprice)
    elif data['command'] == "highprice":
        bot.register_next_step_handler(call.message, highprice)
    elif data['command'] == "bestdeal":
        bot.register_next_step_handler(call.message, bestdeal)
