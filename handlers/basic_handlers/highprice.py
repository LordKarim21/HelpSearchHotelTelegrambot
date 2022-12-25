from typing import Dict, List
from telebot.types import Message, InputMediaPhoto
from config_data.contact_information import User
from database.user_data import set_history
from loader import bot
from utils.city.city_list import get_inline_city
from utils.data_work.get_data_hotel_detail import get_data
from utils.img.get_img import get_image
from utils.request_api.get_detail_hotel import get_hotel_detail
from utils.request_api.hotels_search import hotels_search
from utils.data_work.get_data_hotels import get_data_hotel
from keyboards.inline.create_url_keyboard import get_keyboard_url


@bot.message_handler(commands=['highprice'])
def start_highprice(message: Message):
    data = User.get_data_with_user(message.from_user.id)
    data['command'] = 'highprice'
    data["min_price"] = 150
    data["max_price"] = 300
    msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
    bot.register_next_step_handler(msg, get_inline_city)


def highprice(message: Message):
    print("highprice")
    response_json = hotels_search(get_data_hotel(message))
    data = User.get_data_with_user(message.from_user.id)
    hotels_name_list = []
    if "errors" not in response_json:
        hotels_list: List[Dict] = response_json["data"]["propertySearch"]['properties']
        index_stop = data["hotels_number_to_show"]
        for hotel in hotels_list[:index_stop]:
            property_id = hotel['id']
            keyboard = get_keyboard_url(property_id)
            data['property_id'] = property_id
            hotel_name = hotel['name']
            hotels_name_list.append(hotel_name)
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
                bot.send_message(message.from_user.id, text, reply_markup=keyboard)
        set_history(command_name=data['command'],
                    hotels_name=', '.join(hotels_name_list), user_id=message.from_user.id)
    else:
        bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
        errors_message = response_json['errors'][0]['message']
        code = response_json['errors'][0]['extensions']['code']
        if errors_message == "'Execute GraphQL failed.'":
            raise Exception(code, errors_message)
