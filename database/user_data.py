from datetime import datetime
from typing import Dict, List

from database.models import UserData, History


def _add_user_data(user_telegram_id: int) -> None:
    UserData.create(user_telegram_id=user_telegram_id)


def _exists_user(user_id: int) -> bool:
    users = UserData.select().where(user_id == UserData.user_telegram_id)
    if users:
        return True
    else:
        return False


def _get_in_date(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.in_date


def _get_out_date(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.out_date


def _get_region_id(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.regionId


def _get_hotel(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.hotels_name, user.hotel_id


def _get_city(user_id: int):
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.city_name, user.city_id


def _get_adults(user_id: int) -> int:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.adults


def _get_children(user_id: int) -> List[int]:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    children_list = [int(i) for i in user.children.split(', ')] if "," in user.children else int(user.children)
    return children_list


def _set_children(user_id: int, children_list: List) -> None:
    if len(children_list) > 1:
        children = ", ".join(children_list)
    else:
        children = children_list[0]
    UserData.update({UserData.children: children}).where(user_id == UserData.user_telegram_id).execute()


def _get_lang(user_id) -> str:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.lang


def _get_cur(user_id) -> str:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.current


def _get_command(user_id) -> str:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    return user.user_command


def _set_lang(user_id: int, lang: str) -> None:
    UserData.update({UserData.lang: lang}).where(user_id == UserData.user_telegram_id).execute()


def _set_command(user_id: int, command: str) -> None:
    UserData.update({UserData.user_command: command}).where(user_id == UserData.user_telegram_id).execute()


def _set_cur(user_id: int, cur: str) -> None:
    UserData.update({UserData.current: cur}).where(user_id == UserData.user_telegram_id).execute()


def _set_adults(user_id: int, adults: Dict) -> None:
    UserData.update({UserData.adults: adults}).where(user_id == UserData.user_telegram_id).execute()


def _set_city(user_id: int, city_name: str, city_id: int) -> None:
    UserData.update({
        UserData.city_name: city_name,
        UserData.city_id: city_id
    }).where(user_id == UserData.user_telegram_id).execute()


def _set_hotels(user_id: int, hotels_name: str, hotels_id) -> None:
    UserData.update({
        UserData.hotels_name: hotels_name,
        UserData.hotels_id: hotels_id
    }).where(user_id == UserData.user_telegram_id).execute()
    _set_history(user_id, hotel_name=hotels_name)


def _set_region_id(user_id: int, region_id: int) -> None:
    UserData.update({UserData.regionId: region_id}).where(user_id == UserData.user_telegram_id).execute()


def _set_in_date(user_id: int, in_date: str) -> None:
    UserData.update({UserData.inDate: in_date}).where(user_id == UserData.user_telegram_id).execute()


def _set_out_date(user_id: int, out_date: str) -> None:
    UserData.update({UserData.outDate: out_date}).where(user_id == UserData.user_telegram_id).execute()


def _set_history(user_id, hotel_name) -> None:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()
    History.create(user=user.user_telegram_id, hotel_name=hotel_name, time_request=datetime.now())


def _show_history(user_id: int) -> str:
    user = UserData.select().where(user_id == UserData.user_telegram_id).get()

    history = History.select().where(History.user == user.user_telegram_id)
    if history:
        history_to_show = []
        for row in history:
            history_to_show.append(f"Дата и время обращения: {row.time_request}\n"
                                   f"Список найденных отелей:{row.hotel_name}\n")
    else:
        history_to_show = 'Ваша история поиска пуста!'

    return history_to_show
