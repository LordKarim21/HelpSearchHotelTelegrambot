from keyboards.reply.contanct import request_contact
from states.contact_information import UserInfoState
from utils.request_api.response import hotels_search, location_search
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from loader import bot
from keyboards.inline.city_inline import get_keyboard_city
from utils.request_api.date import get_date


@bot.message_handler(commands=['bestdeal'])
def bestdeal(params):
    response = hotels_search(params=params, timeout=10)
    if response.status_code == 200:
        keyboard = InlineKeyboardMarkup()
        for city in response['sr'][:5]:
            if city["type"] == "hotelId":
                key = InlineKeyboardButton(
                    text=city['regionNames']['fullName'],
                    callback_data='{}=>{}'.format(city['gaiaId'], city['regionNames']['fullName'])
                )
                keyboard.add(key)
        return keyboard
    else:
        return False


def base(message: Message):
    bot.set_state(message.from_user.id, UserInfoState.city, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет, {UserInfoState.name}. Какой город Вас интересует?")


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    temp = bot.send_message(chat_id=message.chat.id,
                            text='Выполняю поиск...', parse_mode='HTML')
    if message.text.isalpha():
        response = location_search(city=message.text, timeout=5)
        if response.status_code == 200:
            question = 'Я нашёл для тебя следующие варианты...'
            keyboard = get_keyboard_city(response.json())
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=temp.id,
                                  text='По вашему запросу ничего не найдено...\n/help', parse_mode='HTML')
    else:
        bot.send_message(message.from_user.id, "Город может содержать только буквы")


@bot.callback_query_handler(func=lambda call: "=>" in call.data)
def set_city(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.message.from_user.id, call.message.chat.id) as data:
        data['city'] = call.data.split("=>")[-1]
    bot.send_message(call.message.from_user.id, "Спасибо, записал. Теперь введи свою дату приезда")
    bot.set_state(call.message.from_user.id, UserInfoState.in_date, call.message.chat.id)


@bot.message_handler(state=UserInfoState.in_date)
def get_in_date(message: Message) -> None:
    date = get_date(message=message)
    cmd, year, month, day = date.split(';')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['in_date'] = {"day": day, "month": month, "year": year}
    bot.send_message(message.from_user.id, "Спасибо, записал. Теперь введи свою дату уиезда")
    bot.set_state(message.from_user.id, UserInfoState.out_date, message.chat.id)


@bot.message_handler(state=UserInfoState.out_date)
def get_out_date(message: Message) -> None:
    date = get_date(message=message)
    cmd, year, month, day = date.split(';')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['in_date'] = {"day": day, "month": month, "year": year}
    bot.send_message(message.from_user.id, "Спасибо, записал. Сколько взрослых поедет?")
    bot.set_state(message.from_user.id, UserInfoState.adults, message.chat.id)


@bot.message_handler(state=UserInfoState.adults)
def get_adults(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['adults'] = message.text
    bot.send_message(
        message.from_user.id,
        "Спасибо, записал. Сколько детей поедет?\n(Пример если поедут двое: 4, 6;Пример если не поедут:\t)"
    )
    bot.set_state(message.from_user.id, UserInfoState.children, message.chat.id)


@bot.message_handler(state=UserInfoState.children)
def get_city(message: Message) -> None:
    count_children = len(message.text.split(", "))
    if count_children > 0 or count_children == 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['children'] = message.text
        bot.send_message(message.from_user.id,
                         "Спасибо, записал. Отправь свой номер телефона нажав кнопку")
        bot.set_state(message.from_user.id, UserInfoState.price, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Возраст детей/ребенка может быть только числом")

        #     "filters": {"price": {
        #         "max": 150,
        #         "min": 100


@bot.message_handler(state=UserInfoState.price)
def get_contact(message: Message) -> None:
    if message.content_type == 'contact':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            text = f"Спасибо за предоставленую информацию ваши данные:\n" \
                   f"Имя - {data['name']}\nВозраст - {data['age']}\n" \
                   f"Страна - {data['country']}\nГород - {data['city']}\n" \
                   f"Номер телефона - {data['phone_number']}"
            bot.send_message(message.from_user.id, text)
    else:
        bot.send_message(message.from_user.id, "Чтобы отправить контактную информацию ножми на кнопку")
