from utils.request_api.response import hotels_search
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot


@bot.message_handler(commands=['highprice'])
def highprice(params):
    response = hotels_search(params=params, timeout=10)
    if response.status_code == 200:
        keyboard = InlineKeyboardMarkup()
        for city in response['sr'][:5]:
            if city["type"] == "hotelId":
                key = InlineKeyboardButton(
                    text=city['regionNames']['fullName'],
                    callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
                )
                keyboard.add(key)
        return keyboard
    else:
        return False
