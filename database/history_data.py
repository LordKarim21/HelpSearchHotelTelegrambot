from datetime import datetime
from typing import List
from database.models import History
from peewee import OperationalError


def clear_history(user_id):
    history_list = History.select().where(user_id == History.user_telegram_id)
    for history in history_list:
        history.delete_instance()


def set_history(user_id: int, hotels_name: str, command_name: str) -> None:
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    History.create(
        time_request=now,
        hotels_name=hotels_name,
        command_name=command_name,
        user_telegram_id=user_id,
    )


def get_history(user_id: int) -> List[str]:
    try:
        users = History.select().where(user_id == History.user_telegram_id)
        if users:
            history_to_show = []
            for history in users:
                history_to_show.append(f"{history.time_request}\n"
                                       f"Команда поиска :{history.command_name}\n"
                                       f"Найденный отели:{history.hotels_name}\n")

        else:
            history_to_show = ['Ваша история поиска пуста!']
    except OperationalError:
        history_to_show = ['Ваша история поиска пуста!']

    return history_to_show
