from typing import List, Dict
from telebot.types import CallbackQuery
from config_data.contact_information import User
from database.user_data import set_history
from keyboards.inline.create_url_keyboard import get_keyboard_url
from utils.data_work.get_data_hotels import get_data_hotel
from utils.hotel_num.hotel_num import get_hotel_num
from loader import bot
from handlers.basic_handlers.best_deal import get_max_price
from utils.photo.question_amount_photo import get_photo_amount
from utils.request_api.hotels_search import hotels_search


@bot.callback_query_handler(func=lambda call: "Id" in call.data)
def get_city(call: CallbackQuery) -> None:
    region_id = call.data.split(":")[1]
    data = User.get_data_with_user(call.from_user.id)
    data['city'] = call.message.text
    data['region_id'] = int(region_id)
    if data['command'] != "bestdeal":
        msg = bot.send_message(call.from_user.id, "Спасибо, записал. Теперь введи число отелей")
        bot.register_next_step_handler(msg, get_hotel_num)
    else:
        msg = bot.send_message(chat_id=call.message.chat.id, text='Введите вашу высокую цену')
        bot.register_next_step_handler(msg, get_max_price)


@bot.callback_query_handler(func=lambda call: call.data in ["True", "False"])
def get_position_photo(call: CallbackQuery) -> None:
    bot.answer_callback_query(callback_query_id=call.id)
    bot.send_message(chat_id=call.message.chat.id, text="Все готово")
    if call.data == "True":
        msg = bot.send_message(call.from_user.id, "Введите количество фотографий")
        bot.register_next_step_handler(msg, get_photo_amount)
    else:
        response_json = hotels_search(get_data_hotel(call.message))
        data = User.get_data_with_user(call.from_user.id)
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
                bot.send_message(call.from_user.id, text, reply_markup=keyboard)
            set_history(command_name=data['command'],
                        hotels_name=', '.join(hotels_name_list), user_id=call.from_user.id)
        else:
            bot.send_message(call.from_user.id, "Ошибка, попбробуйте снова позже")
            errors_message = response_json['errors'][0]['message']
            code = response_json['errors'][0]['extensions']['code']
            if errors_message == "'Execute GraphQL failed.'":
                raise Exception(code, errors_message)
