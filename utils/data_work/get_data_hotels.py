from typing import Dict
from database.user_data import get_command, get_arrival_date, get_departure_date, get_region_id, get_max_price, \
    get_min_price


def get_data_hotel(user_id: int) -> Dict:
    cmd: str = get_command(user_id)
    if cmd == 'lowprice':
        sort = "PRICE_LOW_TO_HIGH"
    elif cmd == 'highprice':
        sort = "PROPERTY_CLASS"
    else:
        sort = "DISTANCE"
    min_price, max_price = (int(get_min_price(user_id)), int(get_max_price(user_id))) \
        if get_min_price(user_id) < get_max_price(user_id) else (get_max_price(user_id), int(get_min_price(user_id)))
    in_date_year, in_date_month, in_date_day = get_arrival_date(user_id).split("-")
    out_date_year, out_date_month, out_date_day = get_departure_date(user_id).split("-")
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "destination": {
            "regionId": str(get_region_id(user_id))
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
                "max": max_price,
                "min": min_price
            }
        }
    }
    return payload
