from typing import Dict
from typing import List
from telebot.types import Message
from loader import bot
from config_data.contact_information import User
from utils.city.city_list import get_inline_city
from utils.img.get_img import get_image
from utils.request_api.hotels_search import hotels_search
from utils.data_work.get_data_hotels import get_data


@bot.message_handler(commands=['lowprice'])
def start_lowprice(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'lowprice'
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)


# Для команд lowprice, highprice и bestdeal сообщение с результатом команды должно
# содержать краткую информацию по каждому отелю. В эту информацию как минимум
# входит:
# ● название отеля,
# ● адрес,
# ● как далеко расположен от центра,
# ● цена,
# ● N фотографий отеля (если пользователь счёл необходимым их вывод)


def lowprice(message: Message):
    response_json = hotels_search(get_data(message))
    data = User.get_data_with_user(message.from_user.id)
    if "errors" not in response_json:
        print(response_json)
        hotels_list: List[Dict] = response_json["data"]["propertySearch"]['properties']
        index_stop = data["hotels_number_to_show"]
        for hotel in hotels_list[:index_stop]:
            hotel_name = hotel['name']
            lat_long = str(hotel["mapMarker"]['latLong']['longitude']) + " miles"
            neighborhood = hotel['neighborhood']['name']
            price = hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"]
            text = f"Название {hotel_name}, Район: {neighborhood}," \
                   f" Kак далеко расположен от центра: {lat_long}, Цена: {price}"
            if data['photos_uploaded']['status']:
                hotel_image = hotel["propertyImage"]['image']["url"]
                bot.send_photo(message.chat.id, get_image(hotel_image), text)
            else:
                bot.send_message(message.from_user.id, text)
    else:
        errors_message = response_json['errors'][0]['message']
        code = response_json['errors'][0]['extensions']['code']
        print(f"Название ошибки {errors_message}, причина ошибки {code}")
        print(response_json)
    print("Конец")
