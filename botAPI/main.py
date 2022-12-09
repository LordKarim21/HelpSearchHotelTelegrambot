"""
Файл для запуска бота
"""
import calendar
from calend import create_calendar, _get_years, _get_month, _valid_year, _valid_month, _valid_date
from loader import exception_handler
from telebot import types, TeleBot, apihelper
from database.user_data import add_user_data, set_cur, show_history, get_region_id, get_adults, get_children, \
    exists_user, get_command, set_command, set_in_date, set_out_date, get_in_date, set_city, get_cur, get_lang
from API_site.main import location_search
from API_site.bestdeal import bestdeal
from API_site.low_price import lowprice
from API_site.high_price import highprice
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


@bot.callback_query_handler(func=lambda call: "=>" in call.data)
def call_city(call: types.CallbackQuery):
    city_id, city_name = call.data.split("=>")
    set_city(user_id=call.from_user.id, city_name=city_name, city_id=city_id)
    msg = bot.send_message(call.message.from_user.id, text='Какой отель Вас интересует?')
    bot.register_next_step_handler(msg, in_date)


@exception_handler
def search_city(message: types.Message) -> None:
    """
    Проверка параметров настроек, обработка запроса пользователя по поиску города,
    вывод Inline клавиатуры с результатами
    """
    temp = bot.send_message(chat_id=message.chat.id,
                            text='Выполняю поиск...', parse_mode='HTML')
    response = location_search(user_id=message.from_user.id, city=message.text, timeout=5)
    print(response)
    if response.status_code == 200:
        keyboard = types.InlineKeyboardMarkup()
        question = 'Я нашёл для тебя следующие варианты...'
        for city in response['sr'][:5]:
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
    keyboard = _get_years()
    bot.send_message(message.chat.id, text='Уточните год заезда', reply_markup=keyboard)


def out_date(message):
    keyboard = _get_years()
    bot.send_message(message.chat.id, text='Уточните год узаезда', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call:
                            _valid_year(str(call.data)) or _valid_month(str(call.data)) or _valid_date(call.data))
@exception_handler
def calendar_call(call: types.CallbackQuery) -> None:
    if _valid_year(call.data):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        keyboard = _get_month(call.data)
        bot.send_message(call.message.chat.id, text='Уточните месяц', reply_markup=keyboard)
    elif _valid_month(call.data):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        year = call.data.split()[1]
        month = call.data.split()[0]
        month_num = [num for num, name in enumerate(calendar.month_abbr) if name in month and num][0]
        markup = create_calendar(int(year), month_num)
        bot.send_message(call.message.chat.id, text='Уточните дату:', reply_markup=markup)
    elif _valid_date(call.data):
        noun, year, month, day = call.data.split(";")
        if not get_in_date(call.from_user.id):
            set_in_date(user_id=call.from_user.id, in_date=f"{year}:{month}:{day}")
            bot.register_next_step_handler(call.message, out_date)
        elif get_in_date(call.from_user.id):
            set_out_date(user_id=call.from_user.id, out_date=f"{year}:{month}:{day}")
            bot.register_next_step_handler(call.message, set_info)
        else:
            print("Error date 169 line, bot/main.py")
    else:
        print("Error date 171 line, bot/main.py")
        bot.send_message(chat_id=call.message.chat.id, text="12345")


def set_info(message: types.Message):
    msg = bot.send_message(message.from_user.id, text='Какой город Вас интересует?')
    #  save info children
    #  set_region_id save
    #  set_adults save
    bot.register_next_step_handler(msg, return_command)


def return_command(message):
    temp = bot.send_message(chat_id=message.chat.id,
                            text='Выполняю поиск...', parse_mode='HTML')
    cmd = get_command(message.from_user.id)
    #  get_city and get_hotel
    params = {
        "currency": get_cur(message.from_user.id),
        "eapid": 1,
        "locale": get_lang(message.from_user.id),
        "siteId": 300000001,
        "destination": {"regionId": get_region_id(message.from_user.id)},
        "checkInDate": {
            "day": 10,
            "month": 10,
            "year": 2022
        },
        "checkOutDate": {
            "day": 15,
            "month": 10,
            "year": 2022
        },
        "rooms": [
            {
                "adults": get_adults(message.from_user.id),
                "children": get_children(message.from_user.id)  # [{"age": 5}, {"age": 7}]
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": "PRICE_LOW_TO_HIGH",
    }
    if 'highprice' in cmd:
        params['filters'] = {"price": {
            "max": 150,
            "min": 100
        }}
        keyboard = highprice(params)
        if keyboard:
            question = 'Я нашёл для тебя следующие варианты...'

            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                                  text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
        # bot.register_next_step_handler(message, return_command)
    elif 'lowprice' in cmd:
        params['filters'] = {"price": {
            "max": 150,
            "min": 100
        }}
        keyboard = lowprice(params)
        if keyboard:
            question = 'Я нашёл для тебя следующие варианты...'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                                  text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
        # bot.register_next_step_handler(message, return_command)
    elif 'bestdeal' in cmd:
        params['filters'] = {"price": {
            "max": 150,
            "min": 100
        }}
        keyboard = bestdeal(params)
        if keyboard:
            question = 'Я нашёл для тебя следующие варианты...'
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                                  text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
        # bot.register_next_step_handler(message, return_command)


@bot.message_handler(content_types=['text'])
@exception_handler
def random_text(message) -> None:
    bot.send_message(message.chat.id, "Я Вас не понимаю.\nВведите команду: /help")





if __name__ == '__main__':
    bot.polling(none_stop=True)
