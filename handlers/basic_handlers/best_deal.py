from typing import Dict, List
from telebot.types import Message
from config_data.contact_information import User
from loader import bot
from utils.city.city_list import get_inline_city
from utils.hotel_num.hotel_num import get_hotel_num
from utils.img.get_img import get_image
from utils.request_api.hotels_search import hotels_search
from utils.data_work.get_data_hotels import get_data


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


# 4. Количество отелей, которые необходимо вывести в результате (не больше
# заранее определённого максимума).
# 5. Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)
# a. При положительном ответе пользователь также вводит количество
# необходимых фотографий (не больше заранее определённого
# максимума)

# Для команд lowprice, highprice и bestdeal сообщение с результатом команды должно
# содержать краткую информацию по каждому отелю. В эту информацию как минимум
# входит:
# ● название отеля,
# ● адрес,
# ● как далеко расположен от центра,
# ● цена,
# ● N фотографий отеля (если пользователь счёл необходимым их вывод)


def bestdeal(message: Message):  # Поменят
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
        bot.send_message(message.from_user.id, "Ошибка, попбробуйте снова позже")
        errors_message = response_json['errors'][0]['message']
        code = response_json['errors'][0]['extensions']['code']
        raise errors_message(code)
