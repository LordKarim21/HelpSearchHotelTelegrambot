from typing import Dict
from telebot.types import Message
from config_data.contact_information import User
from datetime import datetime


def get_data_hotel(message: Message) -> Dict:
    data = User.get_data_with_user(message.from_user.id)
    if data['command'] == 'lowprice':
        sort = "PRICE_LOW_TO_HIGH"
    elif data['command'] == 'highprice':
        sort = "PROPERTY_CLASS"
    else:
        sort = "RECOMMENDED"
    payload = {
        "currency": 'USD',
        "eapid": 1,
        "locale": 'en_US',
        "siteId": 300000001,
        "destination": {
            "regionId": str(data["region_id"])
        },
        "checkInDate": {
            "day": int(datetime.now().day),
            "month": int(datetime.now().month),
            "year": int(datetime.now().year)
        },
        "checkOutDate": {
            "day": int(datetime.now().day) + 5,
            "month": int(datetime.now().month),
            "year": int(datetime.now().year)
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
                "max": int(data['max_price']),
                "min": int(data['min_price'])
            }
        }
    }
    return payload
