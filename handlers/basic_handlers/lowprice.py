from telebot.types import Message
from loader import bot
from config_data.contact_information import User
from utils.city.city_list import get_inline_city


@bot.message_handler(commands=['lowprice'])
def start_lowprice(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'lowprice'
    data["min_price"] = 10
    data["max_price"] = 150
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)
