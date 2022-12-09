from typing import Dict
from main import hotels_search
from database.user_data import get_lang, get_cur


def highprice(user_city_id: str, user_id: int, hotels_value: int, InDate: Dict, OutDate: Dict,
              regionId: int, rooms: Dict):
    filters = {}
    # rooms = [{
    #         "adults": 2,
    #         "children": [{"age": 5}, {"age": 7}]
    # }]
    params = {
        'currency': get_cur(user_id), "eapid": 1, "siteId": user_city_id, 'locale': get_lang(user_id),
        "destination": {"regionId": regionId},
        "checkInDate": InDate, "checkOutDate": OutDate, "rooms": rooms,
        "filters": filters, "resultsStartingIndex": 0, "resultsSize": hotels_value, "sort": "PRICE_LOW_TO_HIGH",
    }
    response = hotels_search(params=params, timeout=10)
