from typing import List, Dict
from telebot.types import Message
from database.history_data import set_history
from database.user_data import get_hotels_number_to_show, set_property_id, get_command
from keyboards.inline.create_url_keyboard import get_keyboard_url
from loader import bot
from utils.data_work.get_data_hotels import get_data_hotel
from utils.request_api.hotels_search import hotels_search


def response_hotels(message: Message, user_id: int):
    bot.send_message(chat_id=message.chat.id, text="Все готово")
    try:
        response_json = hotels_search(get_data_hotel(message.from_user.id))
    except Exception:
        response_json = hotels_search(get_data_hotel(user_id))
    if response_json is not None:
        bot.send_message(chat_id=message.chat.id, text="Все готово")
        hotels_name_list = []
        if "errors" not in response_json:
            hotels_list: List[Dict] = response_json["data"]["propertySearch"]['properties']
            index_stop = get_hotels_number_to_show(message.from_user.id)
            for hotel in hotels_list[:index_stop]:
                property_id = hotel['id']
                keyboard = get_keyboard_url(property_id)
                set_property_id(message.from_user.id, property_id)
                hotel_name = hotel['name']
                hotels_name_list.append(hotel_name)
                lat_long = str(hotel["mapMarker"]['latLong']['longitude']) + " miles"
                # neighborhood = hotel['neighborhood']['name']
                price = hotel["price"]["displayMessages"][0]["lineItems"][0]["price"]["formatted"]
                text = f"Название: {hotel_name}\nKак далеко расположен от центра: {lat_long}" \
                       f"\nЦена: {price}"  # Район
                bot.send_message(message.from_user.id, text, reply_markup=keyboard)
            set_history(command_name=get_command(message.from_user.id),
                        hotels_name=', '.join(hotels_name_list), user_id=message.from_user.id)
        else:
            bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
    else:
        bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
