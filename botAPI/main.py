"""
Файл для запуска бота
"""
import calendar
from typing import List
from calend import create_calendar, _get_years, _get_month, _valid_year, _valid_month, _valid_date
import re
from loader import exception_handler
from telebot import types, TeleBot, apihelper
from database.user_data import add_user_data, set_cur, show_history, set_lang, \
    get_lang, exists_user, get_cur, get_command, set_command, set_in_date, set_out_date, get_out_date, get_in_date, \
    set_city
from API_site.main import location_search

my_token = "5944450117:AAFY1rxjupBwRZ4P7BmfY2JcjgOT23GIdBk"
bot = TeleBot(my_token)
bot.set_webhook()


@bot.callback_query_handler(func=lambda call: call.data in ['RUB', 'USD', 'EUR'])
@exception_handler
def change_cur(call: types.CallbackQuery) -> None:
    """Установка валюты пользователем"""
    set_cur(user_id=call.message.chat.id, cur=call.data)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.message_handler(commands=['settings'])
@exception_handler
def command_settings(message: types.Message):
    question = 'Установить валюту по умолчанию:'
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for currency in ['RUB', 'USD', 'EUR']:
        key = types.InlineKeyboardButton(text=currency, callback_data=currency)
        keyboard.add(key)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    check_state_inline_keyboard(message=message)


@bot.message_handler(commands=['help'])
@exception_handler
def command_help(message: types.Message) -> None:
    answer_message = 'Привет {}! Добро пожаловать!'.format(
        message.from_user.first_name
    )
    answer_message += "\n" + "Сведения о командах\n/help - помощь по командам\n"\
                             "/lowprice — вывод самых дешёвых отелей в городе\n"\
                             "/highprice — вывод самых дорогих отелей в городе\n"\
                             "/bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n"\
                             "/history — вывод истории поиска отелей\n"\
                             "/settings — Установка параметров поиска (язык, валюта)"
    bot.send_message(message.from_user.id, text=answer_message)


@bot.message_handler(commands=['start'])
@exception_handler
def start_message(message: types.Message) -> None:
    """Стартовое сообщение"""
    if not exists_user(message.from_user.id):
        add_user_data(message.from_user.id)
    answer = "Добрый день! \nЯ - бот по поиску отелей\nДля получения информации о командах нажмите /help"
    bot.send_message(message.from_user.id, text=answer)


@bot.message_handler(commands=['highprice', 'lowprice', 'bestdeal'])
@exception_handler
def get_cmd(message: types.Message):
    set_command(message.from_user.id, message.text)
    check_city(message)


@exception_handler
def check_city(message: types.Message):
    msg = bot.send_message(message.from_user.id, text='Какой город Вас интересует?')
    bot.register_next_step_handler(msg, search_city)


@bot.callback_query_handler(func=lambda call: True)
def call_city(call: types.CallbackQuery):
    set_city(call.from_user.id, city_name=call.data)


@exception_handler
def search_city(message: types.Message) -> None:
    """Проверка параметров настроек, обработка запроса пользователя по поиску города,
    вывод Inline клавиатуры с результатами"""
    temp = bot.send_message(chat_id=message.chat.id,
                            text='Выполняю поиск...', parse_mode='HTML')
    response = location_search(user_id=message.from_user.id, city=message.text, timeout=5)
    keyboard = types.InlineKeyboardMarkup()
    question = 'Я нашёл для тебя следующие варианты...'
    if response.status_code == 200:
        answer = response.json()
        for city in answer['sr']:
            if city["type"] == "CITY":
                key = types.InlineKeyboardButton(
                    text=city['regionNames']['fullName'],
                    callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
                )
                keyboard.add(key)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                              text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')


@bot.message_handler(commands=['history'])
@exception_handler
def command_history(message: types.Message) -> None:
    bot.send_message(message.chat.id, show_history(message.from_user.id))


@exception_handler
def check_state_inline_keyboard(message: types.Message) -> None:
    """
    Функция -  предназначена для удаления inline-кнопок, в случае не активного статуса
    (пользователь перешёл в другую команду). Чтобы исключить повторное нажатие на кнопку вне сценария,
    данная функция удаляет оставшиеся inline-кнопки, если кнопки нет, то возникает исключение
    ApiTelegramException, которое функция подавляет.

    :param message: Message
    :return: None
    """
    try:
        bot.edit_message_reply_markup(message.chat.id, message.message_id)
    except apihelper.ApiTelegramException:
        pass
    except AttributeError:
        pass


def in_date(message):
    keyboard = get_year()
    bot.send_message(message.chat.id, text='Уточните год заезда', reply_markup=keyboard)


def get_year():
    years_list = _get_years()
    keyboard = types.InlineKeyboardMarkup()
    for year in years_list:
        key = types.InlineKeyboardButton(text=str(year), callback_data=year)
        keyboard.add(key)
    return keyboard


def out_date(message):
    keyboard = get_year()
    bot.send_message(message.chat.id, text='Уточните год узаезда', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:
                            _valid_year(str(call.data)) or _valid_month(str(call.data)) or _valid_date(call.data))
@exception_handler
def calendar_call(call: types.CallbackQuery) -> None:
    """Установка валюты пользователем"""

    if _valid_year(call.data):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        year = call.data
        months_list: List[str] = _get_month()
        keyboard = types.InlineKeyboardMarkup()
        for month in months_list:
            key = types.InlineKeyboardButton(text=month, callback_data=" ".join((month, year)))
            keyboard.add(key)
        bot.send_message(call.message.chat.id, text='Уточните месяц заезда', reply_markup=keyboard)
    elif _valid_month(call.data):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        year = call.data.split()[1]
        month = call.data.split()[0]
        month_num = [num for num, name in enumerate(calendar.month_abbr) if name in month and num][0]
        markup = create_calendar(int(year), month_num)
        bot.send_message(call.message.chat.id, text='Уточните дату заезда:', reply_markup=markup)
    elif _valid_date(call.data):
        noun, year, month, day = call.data.split(";")
        if not get_in_date(user_id=call.from_user.id):
            set_in_date(user_id=call.from_user.id, in_date=f"{year}:{month}:{day}")
        elif not get_out_date(call.from_user.id):
            set_out_date(user_id=call.from_user.id, out_date=f"{year}:{month}:{day}")
        bot.send_message(chat_id=call.message.chat.id, text="Супер")
    else:
        bot.send_message(chat_id=call.message.chat.id, text="12345")


@bot.message_handler(content_types=['text'])
@exception_handler
def random_text(message) -> None:
    bot.send_message(message.chat.id, "Я Вас не понимаю.\nВведите команду: /help")


#####################################################################################################


def check_params(chat_id, text):
    pass


def flag_advanced_question(id_q):
    pass


def ask_for_hotels_value(message):
    pass


def city_handler(call: types.CallbackQuery) -> None:
    """Обработка данных искомого города (id, name), определение следующего шага обработчика"""
    set_city(call.message.chat.id, call.data)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    if flag_advanced_question(call.message.chat.id):
        ask_for_price_range(call.message)
    else:
        ask_for_hotels_value(call.message)


def set_price_range(chat_id, value):
    pass


def ask_for_dist_range(message: types.Message) -> None:
    """Обработка значений ценового диапазона пользователя, запрос диапазона дистанции,
    определение следующего шага обработчика"""
    price_range = list(set(map(int, map(lambda string: string.replace(',', '.'),
                                        re.findall(r'\d+[.,\d+]?\d?', message.text)))))
    if len(price_range) != 2:
        raise ValueError('Range Error')
    else:
        set_price_range(chat_id=message.chat.id, value=price_range)
        bot.send_message(chat_id=message.chat.id,
                         text='Уточните диапазон расстояния, на котором находится отель от центра (км):'
                              '\n(Например: "от 1 до 3" / "1-3" / "1 3")')
        bot.register_next_step_handler(message, ask_for_hotels_value)


def ask_for_price_range(message: types.Message) -> None:
    """Запрос ценового диапазона у пользователя, определение следующего шага обработчика"""
    cur = get_cur(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text=f'Уточните ценовой диапазон ({cur})'
                                                   f'\n(Например: "от 1000 до 2000", "1000-2000", "1000 2000")')
    bot.register_next_step_handler(message, ask_for_dist_range)


def set_hotels_value(chat_id, value):
    pass


def photo_needed(message: types.Message) -> None:
    """Обработка значения кол-ва отелей пользователя, запрос необходимости вывода фото в виде Inline клавитуары"""
    set_hotels_value(chat_id=message.chat.id, value=abs(int(message.text)))
    keyboard = types.InlineKeyboardMarkup()
    [keyboard.add(types.InlineKeyboardButton(x, callback_data=x)) for x in
     ['Да', 'Нет']]
    bot.send_message(message.chat.id, text='Интересуют фотографии объектов?',
                     reply_markup=keyboard)


def set_needed_photo(chat_id, value):
    pass


# @bot.callback_query_handler(
#     func=lambda call: _['photo_needed'] in call.message.text)
# def set_photo_needed(call: types.CallbackQuery) -> None:
#     """Обработка ответа пользователя о необходимости вывода фото, определение хода действий."""
#     bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
#     if any(call.data in answer for answer in _['pos'].values()):
#         set_needed_photo(chat_id=call.message.chat.id, value=True)
#         number_of_photo(call.message)
#     else:
#         set_needed_photo(chat_id=call.message.chat.id, value=False)
#         result(call.message)


# def number_of_photo(message: types.Message) -> None:
#     """Запрос кол-ва фото у пользователя, определение следующего шага обработчика"""
#     bot.send_message(chat_id=message.chat.id,
#                      text=_['photos_value'])
#     bot.register_next_step_handler(message, result)


def get_needed_photo(chat_id):
    pass


def set_photos_value(chat_id, value):
    pass


def get_hotels(user_id):
    pass


def get_hotels_value(chat_id):
    pass


# def result(message: types.Message) -> None:
#     """Обработка значения кол-ва фото, выполнение поиска вариантов, представление результатов"""
#     if get_needed_photo(chat_id=message.chat.id):
#         set_photos_value(chat_id=message.chat.id, value=abs(int(message.text)))
#     temp = bot.send_message(chat_id=message.chat.id, text=_['search'])
#     hotels_dict, search_link = get_hotels(user_id=message.chat.id)
#
#     if hotels_dict:
#         bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
#                               text=_['ready_to_result'])
#         for index, i_data in enumerate(hotels_dict.values()):
#             if index + 1 > get_hotels_value(chat_id=message.chat.id):
#                 break
#             text = _['main_results'].format(
#                 name=i_data['name'], address=get_address(i_data), distance=get_landmarks(i_data),
#                 price=i_data['price'], e_hotel=emoji['hotel'], e_address=emoji['address'],
#                 e_dist=emoji['landmarks'], e_price=emoji['price'], e_link=emoji['link'],
#                 link='https://hotels.com/ho' + str(i_data['id']),
#                 address_link='https://www.google.ru/maps/place/' + i_data['coordinate'])
#
#             if get_needed_photo(chat_id=message.chat.id):
#                 photo_list = get_photos(user_id=message.chat.id, hotel_id=int(i_data['id']), text=text)
#                 for i_size in ['z', 'y', 'd', 'n', '_']:
#                     try:
#                         bot.send_media_group(chat_id=message.chat.id, media=photo_list)
#                         break
#                     except apihelper.ApiTelegramException:
#                         photo_list = [types.InputMediaPhoto(caption=obj.caption, media=obj.media[:-5] + f'{i_size}.jpg',
#                                                             parse_mode=obj.parse_mode) for obj in photo_list]
#             else:
#                 bot.send_message(message.chat.id, text, parse_mode='HTML', disable_web_page_preview=True)
#
#         bot.send_message(chat_id=message.chat.id, text=_['additionally'].format(
#             link=search_link), parse_mode='MarkdownV2', disable_web_page_preview=True)
#     else:
#         bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
#                               text=_['no_options'])


if __name__ == '__main__':
    bot.polling(none_stop=True)
