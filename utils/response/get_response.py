from typing import List, Dict
from telebot.types import Message, InputMediaPhoto
from database.history_data import set_history
from database.user_data import get_hotels_number_to_show, set_property_id, get_command, get_photos_status, \
    get_number_of_photos, get_distance_from_center
from keyboards.inline.create_url_keyboard import get_keyboard_url
from loader import bot
from utils.converter.convert_mile_in_km import convert_mile_in_km
from utils.data_work.get_data_hotel_detail import get_data
from utils.data_work.get_data_hotels import get_data_hotel
from utils.img.get_img import get_image
from utils.request_api.get_detail_hotel import get_hotel_detail
from utils.request_api.hotels_search import hotels_search


def response_hotels(message: Message):
    response_json = hotels_search(get_data_hotel(message.chat.id))
    if response_json is not None:
        bot.send_message(chat_id=message.chat.id, text="Все готово")
        hotels_name_list = []
        command_name = get_command(message.chat.id)
        if "errors" not in response_json:
            hotels_list: List[Dict] = response_json["data"]["propertySearch"]['properties']
            index_stop = get_hotels_number_to_show(message.chat.id)
            state_photo = get_photos_status(message.chat.id)
            amount_photo = get_number_of_photos(message.chat.id)
            count_hotels = 0
            for hotel in hotels_list:
                count_hotels += 1
                if count_hotels == index_stop:
                    break
                property_id = hotel['id']
                keyboard = get_keyboard_url(property_id)
                set_property_id(message.chat.id, property_id)
                hotel_name = hotel['name']
                hotels_name_list.append(hotel_name)
                destination_miles = hotel["destinationInfo"]['distanceFromDestination']['value']
                neighborhood = hotel['neighborhood']['name']
                destination_km = convert_mile_in_km(destination_miles)
                price = hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"]
                text = f"Название: {hotel_name}\nKак далеко расположен от центра: {round(destination_km, 2)} км" \
                       f"\nЦена: {price}\nРайон: {neighborhood}"
                if command_name == "bestdeal":
                    if abs(float(get_distance_from_center(message.chat.id))) <= \
                            abs(float(destination_km)):
                        index_stop += 1
                        continue
                if state_photo:
                    images = get_hotel_detail(get_data(property_id))
                    if images is None:
                        continue
                    hotel_images = []
                    for image in images["data"]['propertyInfo']["propertyGallery"]["images"][:amount_photo]:
                        hotel_images.append(InputMediaPhoto(get_image(image['image']["url"])))
                    bot.send_media_group(message.chat.id, hotel_images)
                bot.send_message(message.chat.id, text, reply_markup=keyboard)
            set_history(command_name=command_name,
                        hotels_name=', '.join(hotels_name_list), user_id=message.chat.id)
            bot.send_message(message.chat.id, "Выберите отель")
        else:
            bot.send_message(message.chat.id, "Ошибка, попбробуйте снова позже")
    else:
        bot.send_message(message.chat.id, "Ошибка, попбробуйте снова позже")
