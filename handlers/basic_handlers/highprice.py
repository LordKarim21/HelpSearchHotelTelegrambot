from telebot.types import Message
from config_data.contact_information import User
from loader import bot
from utils.city.city_list import get_inline_city


@bot.message_handler(commands=['highprice'])
def start_highprice(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'highprice'
    data["min_price"] = 150
    data["max_price"] = 300
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)
