from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    name = State()
    age = State()
    adults = State()
    country = State()
    city = State()
    children = State()
    phone_number = State()
    language = State()
    currency = State()
    in_date = State()
    out_date = State()
    price = State()
