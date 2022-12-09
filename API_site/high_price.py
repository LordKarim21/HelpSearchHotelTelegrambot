from telebot import types
from main import hotels_search


def highprice(params):
    response = hotels_search(params=params, timeout=10)
    if response.status_code == 200:
        keyboard = types.InlineKeyboardMarkup()
        for city in response['sr'][:5]:
            if city["type"] == "hotelId":
                key = types.InlineKeyboardButton(
                    text=city['regionNames']['fullName'],
                    callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
                )
                keyboard.add(key)
        return keyboard
    else:
        return False
