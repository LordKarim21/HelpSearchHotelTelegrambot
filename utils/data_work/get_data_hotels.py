from typing import Dict
from telebot.types import Message
from database.user_data import get_command, get_arrival_date, get_departure_date, get_region_id, get_max_price, \
    get_min_price


def get_data_hotel(message: Message) -> Dict:
    cmd: str = get_command(message.from_user.id)
    if cmd == 'lowprice':
        sort = "PRICE_LOW_TO_HIGH"
    elif cmd == 'highprice':
        sort = "PROPERTY_CLASS"
    else:
        sort = "RECOMMENDED"
    in_date_year, in_date_month, in_date_day = get_arrival_date(message.from_user.id).split("-")
    out_date_year, out_date_month, out_date_day = get_departure_date(message.from_user.id).split("-")
    payload = {
        "currency": 'USD',
        "eapid": 1,
        "locale": 'en_US',
        "siteId": 300000001,
        "destination": {
            "regionId": get_region_id(message.from_user.id)
        },
        "checkInDate": {
            "day": int(in_date_day),
            "month": int(in_date_month),
            "year": int(in_date_year)
        },
        "checkOutDate": {
            "day": int(out_date_day),
            "month": int(out_date_month),
            "year": int(out_date_year)
        },
        "rooms": [
            {
                "adults": 1
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        "sort": sort,
        "filters": {
            "price": {
                "max": get_max_price(message.from_user.id),
                "min": get_min_price(message.from_user.id)
            }
        }
    }
    return payload
