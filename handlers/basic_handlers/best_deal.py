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


def get_min_price(message: Message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введите вашу низкую цену')
    if msg.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['min_price'] = msg.text
        bot.register_next_step_handler(msg, get_range_distance)


def get_range_distance(message: Message):
    msg = bot.send_message(chat_id=message.chat.id, text='Введите на сколько отель может быть далеко от центра')
    if msg.text.isdigit():
        data = User.get_data_with_user(message.from_user.id)
        data['distance_from_center'] = msg.text
        bot.register_next_step_handler(msg, get_hotel_num)


# Команда /bestdeal
# После ввода команды у пользователя запрашивается:
# 1. Город, где будет проводиться поиск.
# 2. Диапазон цен.
# 3. Диапазон расстояния, на котором находится отель от центра.
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
        errors_message = response_json['errors'][0]['message']
        code = response_json['errors'][0]['extensions']['code']
        print(f"Название ошибки {errors_message}, причина ошибки {code}")
    print("Конец")




# def survey(message: Message) -> None:
#     bot.set_state(message.from_user.id, UserInfoState.name, message.chat.id)
#     bot.send_message(message.from_user.id, f"Привет, {message.from_user.username} введи свое имя")
#
#
# @bot.message_handler(state=UserInfoState.name)
# def get_name(message: Message) -> None:
#     if message.text.isalpha():
#         bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи свой возраст")
#         bot.set_state(message.from_user.id, UserInfoState.age, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             print(data)
#             data['name'] = message.text
#     else:
#         bot.send_message(message.from_user.id, "Имя может содержать только буквы")
#
#
# @bot.message_handler(state=UserInfoState.age)
# def get_age(message: Message) -> None:
#     if message.text.isdigit():
#         bot.send_message(message.from_user.id,
#                          "Спасибо, записал. Отправь свой номер телефона нажав кнопку", reply_markup=request_contact())
#         bot.set_state(message.from_user.id, UserInfoState.phone_number, message.chat.id)
#
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['age'] = message.text
#     else:
#         bot.send_message(message.from_user.id, "Возраст может быть только числом")
#
#
# @bot.message_handler(content_types=['contact'], state=UserInfoState.phone_number)
# def get_contact(message: Message) -> None:
#     if message.content_type == 'contact':
#         msg = bot.send_message(chat_id=message.chat.id, text='Введите город где будем искать отель')
#         bot.register_next_step_handler(msg, get_inline_city)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['phone_number'] = message.contact.phone_number
#
#     else:
#         bot.send_message(message.from_user.id, "Чтобы отправить контактную информацию ножми на кнопку")
#
#
# def get_inline_city(message: Message):
#     temp = bot.send_message(chat_id=message.chat.id, text='Выполняю поиск...', parse_mode='HTML')
#     response = location_search(city=message.text, timeout=5)
#     print(response.json())
#     if int(response.status_code) == 200:
#         question = 'Я нашёл для тебя следующие варианты...'
#         keyboard = get_keyboard_city(response.json())
#         bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
#         bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
#     else:
#         bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
#                               text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
#
#
# @bot.message_handler(state=UserInfoState.city)
# @bot.callback_query_handler(func=lambda call: "=>" in call.data)
# def get_city(call: CallbackQuery) -> None:
#     keyboard = calendar_process.create_calendar()
#     bot.send_message(call.from_user.id, "Спасибо, записал. Теперь введи свою дату приезда", reply_markup=keyboard)
#     bot.set_state(call.from_user.id, UserInfoState.in_date, call.message.chat.id)
#     region_id, city = call.data.split("=>")
#     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#         data['trip_city'] = str(city)
#         data['region_id'] = str(region_id)
#
#
# @bot.message_handler(state=UserInfoState.in_date)
# @bot.callback_query_handler(func=lambda call: validate(call.data))
# def get_in_date(call: CallbackQuery) -> None:
#     keyboard = calendar_process.create_calendar()
#     bot.send_message(call.from_user.id, "Спасибо, записал. Теперь введи свою дату уиезда", reply_markup=keyboard)
#     bot.set_state(call.from_user.id, UserInfoState.out_date, call.message.chat.id)
#     calendar_title, action, year, month, day = call.data.split(':')
#     result = calendar_process.calendar_query_handler(
#         bot, call, name=calendar_title, action=action, year=year, month=month, day=day
#     )
#     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#         data['in_date'] = {"day": result.day, "month": result.month, "year": result.year}
#
#
# @bot.message_handler(state=UserInfoState.out_date)
# @bot.callback_query_handler(func=lambda call: validate(call.data))
# def get_out_date(call: CallbackQuery) -> None:
#     bot.send_message(call.from_user.id, "Спасибо, записал. Сколько взрослых поедет?")
#     bot.set_state(call.from_user.id, UserInfoState.adults, call.message.chat.id)
#     calendar_title, action, year, month, day = call.data.split(':')
#     result = calendar_process.calendar_query_handler(
#         bot, call, name=calendar_title, action=action, year=year, month=month, day=day
#     )
#     with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
#         data['out_date'] = {"day": result.day, "month": result.month, "year": result.year}
#
#
# @bot.message_handler(state=UserInfoState.adults)
# def get_adults(message: Message) -> None:
#     if message.text.isdigit():
#         bot.send_message(
#             message.from_user.id,
#             "Спасибо, записал. Сколько детей поедет?\n"
#             "(Пример если поедет один: 4\t;Пример если поедут двое: 4, 6;Пример если не поедут:\t)"
#         )
#         bot.set_state(message.from_user.id, UserInfoState.children, message.chat.id)
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             data['adults'] = message.text
#     else:
#         bot.send_message(message.from_user.id, "Число взрослых может быть только числом")
#
#
# @bot.message_handler(state=UserInfoState.children)
# def get_children(message: Message) -> None:
#     print(message)
#     ages = message.text.split(", ")
#     count_children = len(message.text.split(", "))
#     if count_children > 0 or count_children == 0:
#         with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#             if count_children == 0:
#                 data['children'] = 0
#             else:
#                 data['children'] = []
#                 for i in range(count_children):
#                     data['children'].append({'age': ages[i]})
#         bot.send_message(message.from_user.id,
#                          "Спасибо, записал. Отправь свою минимальную и максимальную цену проживания\n"
#                          "(Пример: 150, 100)")
#         bot.set_state(message.from_user.id, UserInfoState.price, message.chat.id)
#     else:
#         bot.send_message(message.from_user.id, "Возраст детей/ребенка может быть только числом")
#
#
# @bot.message_handler(state=UserInfoState.price)
# def get_price(message: Message) -> None:
#     print(message)
#     max_price, min_price = message.text.split(", ")
#     count_price = len(message.text.split(", "))
#     if count_price == 2:
#         if max_price.isdigit() and min_price.isdigit():
#             with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#                 data['price'] = {'max': max_price, 'min': min_price}
#                 text = f"Спасибо за предоставленую информацию ваши данные:\n" \
#                        f"Имя - {data['name']}\nВозраст - {data['age']}\n" \
#                        f"Город - {data['trip_city']}\n" \
#                        f"Дата приезда - {data['in_date']['day']}/{data['in_date']['month']}/" \
#                        f"{data['in_date']['year']}\n" \
#                        f"Дата возвошения - {data['out_date']['day']}/{data['out_date']['month']}/" \
#                        f"{data['out_date']['year']}\n" \
#                        f"Взрослых - {data['adults']}\n" \
#                        f"Детей - {len(data['children'])}\n" \
#                        f"Вами предложенная среднея цена - " \
#                        f"{int((float(data['price']['max']) + float(data['price']['min'])) / 2)}\n"
#                 bot.send_message(message.from_user.id, text)
#         else:
#             bot.send_message(
#                 message.from_user.id,
#                 "Отправить минимальную и максимальную цену проживания числами и через запятую\n(Пример: 150, 100)"
#             )
#     else:
#         bot.send_message(
#             message.from_user.id,
#             "Отправить минимальную и максимальную цену проживания числами и через запятую\n(Пример: 150, 100)"
#         )
#
#         # text = f"Спасибо за предоставленую информацию ваши данные:\n" \
#         #        f"Имя - {data['name']}\nВозраст - {data['age']}\n" \
#         #        f"Страна - {data['country']}\nГород - {data['city']}\n" \
#         #        f"Номер телефона - {data['phone_number']}"
#         # bot.send_message(message.from_user.id, text)
#
