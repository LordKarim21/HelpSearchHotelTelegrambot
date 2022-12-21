from typing import List

from database.models import History
from peewee import OperationalError


def set_history(user_id: int, hotels_name: str, command_name: str) -> None:
    History.create(
        hotels_name=hotels_name,
        command_name=command_name,
        user_telegram_id=user_id,
    )


def get_history(user_id: int) -> List[str]:
    try:
        users = History.select().where(user_id == History.user_telegram_id)
        if users:
            history_to_show = []
            count_history = 1
            for history in users:
                history_to_show.append(f"{count_history}."
                                       f"Дата и время обращения: {history.time_request}\n"
                                       f"Команда поиска :{history.command_name}\n"
                                       f"Найденный отель:{history.hotels_name}\n")
                count_history += 1
        else:
            history_to_show = ['Ваша история поиска пуста!']
    except OperationalError:
        history_to_show = ['Ваша история поиска пуста!']

    return history_to_show
