from typing import Dict, List
from telebot.types import Message, InputMediaPhoto
from config_data.contact_information import User
from loader import bot
from utils.city.city_list import get_inline_city
from utils.data_work.get_data_hotel_detail import get_data
from utils.hotel_num.hotel_num import get_hotel_num
from utils.img.get_img import get_image
from utils.request_api.get_detail_hotel import get_hotel_detail
from utils.request_api.hotels_search import hotels_search
from utils.data_work.get_data_hotels import get_data_hotel


@bot.message_handler(commands=['bestdeal'])
def start_beatdeal(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'bestdeal'
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)


def get_max_price(message: Message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введите вашу высокую цену')
    if msg.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['max_price'] = msg.text
        bot.register_next_step_handler(msg, get_min_price)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='')  # write message
        bot.register_next_step_handler(answer, get_max_price)


def get_min_price(message: Message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введите вашу низкую цену')
    if msg.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['min_price'] = msg.text
        bot.register_next_step_handler(msg, get_range_distance)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='')  # write message
        bot.register_next_step_handler(answer, get_min_price)


def get_range_distance(message: Message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введите на сколько отель может быть далеко от центра')
    if msg.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['distance_from_center'] = msg.text
        bot.register_next_step_handler(msg, get_hotel_num)
    else:
        answer = bot.send_message(chat_id=message.chat.id, text='')  # write message
        bot.register_next_step_handler(answer, get_range_distance)


def bestdeal(message: Message):  # Поменят
    response_json = hotels_search(get_data_hotel(message))
    data = User.get_data_with_user(message.from_user.id)
    if "errors" not in response_json:
        print(response_json)
        hotels_list: List[Dict] = response_json["data"]["propertySearch"]['properties']
        index_stop = data["hotels_number_to_show"]
        for hotel in hotels_list[:index_stop]:
            data['property_id'] = hotel['id']
            hotel_name = hotel['name']
            lat_long = str(hotel["mapMarker"]['latLong']['longitude']) + " miles"
            neighborhood = hotel['neighborhood']['name']
            price = hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"]
            text = f"Название {hotel_name}, Район: {neighborhood}," \
                   f" Kак далеко расположен от центра: {lat_long}, Цена: {price}"
            if data['photos_uploaded']['status']:
                images = get_hotel_detail(get_data(message))
                hotel_images = []
                stop_index = data['photos_uploaded']['number_of_photos']
                for image in images["data"]['propertyInfo']["propertyGallery"]["images"][:stop_index]:
                    hotel_images.append(InputMediaPhoto(get_image(image['image']["url"])))
                bot.send_media_group(message.chat.id, hotel_images, text)
            else:
                bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
        errors_message = response_json['errors'][0]['message']
        code = response_json['errors'][0]['extensions']['code']
        raise errors_message(code)
