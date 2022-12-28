from telebot.types import Message
from loader import bot
from database.user_data import delete_user, create_user, set_command, set_min_price, set_max_price
from utils.city.city_list import get_inline_city


@bot.message_handler(commands=['lowprice'])
def start_lowprice(message: Message):
    delete_user(message.from_user.id)
    create_user(message.from_user.id)
    set_command(message.from_user.id, 'lowprice')
    set_min_price(message.from_user.id, 10)
    set_max_price(message.from_user.id, 150)
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)
