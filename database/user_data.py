from datetime import datetime
from database.models import History


def set_history(user_id: int, hotels_name: str, city_name: str) -> None:
    History.create(
        hotels_name=hotels_name,
        city_name=city_name,
        user_telegram_id=user_id,
        time_request=datetime.now()
    )


def show_history(user_id: int) -> str:
    users = History.select().where(user_id == History.user_telegram_id)
    if users:
        history_to_show = []
        for history in users:
            history_to_show.append(f"Дата и время обращения: {history.time_request}\n"
                                   f"Найденный город:{history.city}\n"
                                   f"Найденный отель:{history.hotel_name}\n")
    else:
        history_to_show = 'Ваша история поиска пуста!'

    return history_to_show
