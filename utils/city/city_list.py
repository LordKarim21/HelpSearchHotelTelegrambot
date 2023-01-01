from telebot.types import Message
from keyboards.inline.city_inline import get_keyboard_city
from loader import bot
from utils.request_api.location_search import location_search


def get_inline_city(message: Message):
    temp = bot.send_message(chat_id=message.chat.id, text='Выполняю поиск...', parse_mode='HTML')
    response = location_search(city=message.text)
    if int(response.status_code) == 200:
        keyboard = get_keyboard_city(response.json())
        if keyboard.keyboard:
            question = 'Я нашёл для тебя следующие варианты...'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                                  text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                              text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
