from datetime import datetime
from typing import Dict, List

from database.models import UserData, History
from dictionary import dictionary as _


def add_user_data(user_telegram_id: int) -> None:
    """
    Функция создает User в базе данных.

    :param user_telegram_id:
    :return:
    """
    UserData.create(user_telegram_id=user_telegram_id, lang='ru_RU')


def exists_user(user_id: int) -> bool:
    """
    Функция проверяет запись в базе данных.

    :param user_id:
    :return: bool
    """
    users = UserData.select().where(user_id == UserData.user_telegram_id)
    if users:
        return True
    else:
        return False


def get_in_date(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.inDate


def get_out_date(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.outDate


def get_region_id(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.regionId


def get_hotel(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.hotels_name, user.hotel_id


def get_city(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.city_name, user.city_id


def get_adults(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.adults


def get_children(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    children_list = [int(i) for i in user.children.split(', ')] if "," in user.children else int(user.children)
    return children_list


def set_children(user_id: int, children_list: List):
    if len(children_list) > 1:
        children = ", ".join(children_list)
    else:
        children = children_list[0]
    UserData.update({UserData.children: children}).where(user_id == UserData.user_telegram_id).execute()


def get_lang(user_id):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.lang


def get_cur(user_id):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.current


def get_command(user_id):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.user_command


def set_lang(user_id: int, lang: str):
    UserData.update({UserData.lang: lang}).where(user_id == UserData.user_telegram_id).execute()


def set_command(user_id: int, command: str):
    UserData.update({UserData.user_command: command}).where(user_id == UserData.user_telegram_id).execute()


def set_cur(user_id: int, cur: str):
    UserData.update({UserData.current: cur}).where(user_id == UserData.user_telegram_id).execute()


def set_adults(user_id: int, adults: Dict):
    UserData.update({UserData.adults: adults}).where(user_id == UserData.user_telegram_id).execute()


def set_city(user_id: int, city_name: str, city_id: int):
    UserData.update({
        UserData.city_name: city_name,
        UserData.city_id: city_id
    }).where(user_id == UserData.user_telegram_id).execute()


def set_hotels(user_id: int, hotels_name: str, hotels_id):
    UserData.update({
        UserData.hotels_name: hotels_name,
        UserData.hotels_id: hotels_id
    }).where(user_id == UserData.user_telegram_id).execute()
    set_history(user_id, hotel_name=hotels_name)


def set_region_id(user_id: int, region_id: int):
    UserData.update({UserData.regionId: region_id}).where(user_id == UserData.user_telegram_id).execute()


def set_in_date(user_id: int, in_date: str):
    UserData.update({UserData.inDate: in_date}).where(user_id == UserData.user_telegram_id).execute()


def set_out_date(user_id: int, out_date: str):
    UserData.update({UserData.outDate: out_date}).where(user_id == UserData.user_telegram_id).execute()


def set_history(user_id, hotel_name):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    History.create(user=user.user_telegram_id, hotel_name=hotel_name, time_request=datetime.now())


def show_history(user_id: int):
    """
    Функция, которая отправляет пользователю историю запросов.

    :param user_id: int
    :return: str, list
    """
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()

    history = History.select().where(History.user == user.user_telegram_id)
    if history:
        history_to_show = []
        for row in history:
            history_to_show.append(f"Дата и время обращения: {row.time_request}\n"
                                   f"Список найденных отелей:{row.hotel_name}\n")
    else:
        history_to_show = _['clr_history']

    return history_to_show
