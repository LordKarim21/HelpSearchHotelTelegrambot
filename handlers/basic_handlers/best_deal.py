from telebot.types import Message
from config_data.contact_information import User
from loader import bot
from utils.city.city_list import get_inline_city
from utils.hotel_num.hotel_num import get_hotel_num


@bot.message_handler(commands=['bestdeal'])
def start_beatdeal(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'bestdeal'
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)


def get_max_price(message: Message):
    if message.text.isdigit():
        msg = bot.send_message(chat_id=message.chat.id, text='Введите вашу низкую цену')
        data = User.get_data_with_user(message.from_user.id)
        data['max_price'] = message.text
        bot.register_next_step_handler(msg, get_min_price)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='Ваша цена должна быть числом')
        bot.register_next_step_handler(answer, get_max_price)


def get_min_price(message: Message):
    if message.text.isdigit():
        msg = bot.send_message(chat_id=message.chat.id, text='Введите на сколько отель может быть далеко от центра')
        data = User.get_data_with_user(message.from_user.id)
        data['min_price'] = message.text
        bot.register_next_step_handler(msg, get_range_distance)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='Ваша цена должна быть числом')
        bot.register_next_step_handler(answer, get_min_price)


def get_range_distance(message: Message):
    if message.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['distance_from_center'] = message.text
        msg = bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи число отелей")
        bot.register_next_step_handler(msg, get_hotel_num)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='Ваша цена должна быть числом')  # write message
        bot.register_next_step_handler(answer, get_range_distance)
