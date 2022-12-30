from database.models import User
from peewee import OperationalError


def exists_user(user_id: int) -> bool:
    try:
        users = User.select().where(user_id == User.user_telegram_id)
        if users:
            return True
        else:
            return False
    except OperationalError:
        return False


def create_user(user_id: int) -> None:
    if not exists_user(user_id):
        User.create(
            user_telegram_id=user_id
        )


def delete_user(user_id: int) -> None:
    if exists_user(user_id):
        users = User.select().where(user_id == User.user_telegram_id)
        for user in users:
            user.delete_instance()


def get_hotels_number_to_show(user_id: int):
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.hotels_number_to_show


def get_property_id(user_id: int) -> int:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.property_id


def get_command(user_id: int) -> str:
    user = User.select().where(user_id == User.user_telegram_id).get()
    return user.command


def get_region_id(user_id: int) -> str:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.region_id


def get_photos_status(user_id: int) -> bool:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.photos_status


def get_number_of_photos(user_id: int) -> int:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.number_of_photos


def get_min_price(user_id: int) -> int:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.max_price


def get_max_price(user_id: int) -> int:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.min_price


def get_distance_from_center(user_id: int) -> str:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return user.distance_from_center


def get_arrival_date(user_id: int) -> str:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return str(user.arrival_date)


def get_departure_date(user_id: int) -> str:
    user = User.select().where(user_id == User.user_telegram_id).order_by(User.id.desc()).get()
    return str(user.departure_date)


def set_hotels_number_to_show(user_id: int, num: int) -> None:
    user = User.update({User.hotels_number_to_show: num}).where(user_id == User.user_telegram_id)
    user.execute()


def set_property_id(user_id: int, property_id: int) -> None:
    user = User.update({User.property_id: property_id}).where(user_id == User.user_telegram_id)
    user.execute()


def set_command(user_id: int, command: str) -> None:
    user = User.update({User.command: command}).where(user_id == User.user_telegram_id)
    user.execute()


def set_region_id(user_id: int, region_id: int) -> None:
    user = User.update({User.region_id: region_id}).where(user_id == User.user_telegram_id)
    user.execute()


def set_photos_status(user_id: int, photos_status: bool) -> None:
    user = User.update({User.photos_status: photos_status}).where(user_id == User.user_telegram_id)
    user.execute()


def set_number_of_photos(user_id: int, number_of_photos: int) -> None:
    user = User.update({User.number_of_photos: number_of_photos}).where(user_id == User.user_telegram_id)
    user.execute()


def set_min_price(user_id: int, min_price: int) -> None:
    user = User.update({User.min_price: min_price}).where(user_id == User.user_telegram_id)
    user.execute()


def set_max_price(user_id: int, max_price: int) -> None:
    user = User.update({User.max_price: max_price}).where(user_id == User.user_telegram_id)
    user.execute()


def set_distance_from_center(user_id: int, distance_from_center: str) -> None:
    user = User.update({User.distance_from_center: distance_from_center}).where(user_id == User.user_telegram_id)
    user.execute()


def set_arrival_date(user_id: int, arrival_date: str) -> None:
    user = User.update({User.arrival_date: arrival_date}).where(user_id == User.user_telegram_id)
    user.execute()


def set_departure_date(user_id: int, departure_date: str) -> None:
    user = User.update({User.departure_date: departure_date}).where(user_id == User.user_telegram_id)
    user.execute()
