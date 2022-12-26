from typing import List, Dict
from telebot.types import Message
from config_data.contact_information import User
from database.user_data import set_history
from keyboards.inline.create_url_keyboard import get_keyboard_url
from loader import bot
from utils.data_work.get_data_hotels import get_data_hotel
from utils.request_api.hotels_search import hotels_search


def get_photo_amount(message: Message):
    if message.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['photos_uploaded']['status'] = True
        data['photos_uploaded']['number_of_photos'] = int(message.text)
        response_json = hotels_search(get_data_hotel(message))
        if response_json is not None:
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
                    # neighborhood = hotel['neighborhood']['name']
                    price = hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"]
                    text = f"Название: {hotel_name}\nKак далеко расположен от центра: {lat_long}" \
                           f"\nЦена: {price}"  # Район
                    bot.send_message(message.from_user.id, text, reply_markup=keyboard)
                set_history(command_name=data['command'],
                            hotels_name=', '.join(hotels_name_list), user_id=message.from_user.id)
                data['distance_from_center'] = 0
            else:
                bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
        else:
            bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
    else:
        answer = bot.send_message(message.from_user.id, "Количесто фотографий дожно быть числом")
        bot.register_next_step_handler(answer, get_photo_amount)
