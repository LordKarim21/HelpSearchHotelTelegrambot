from typing import Dict
from config_data import config
import requests


def get_hotel_detail(params: Dict):
    method = "POST"
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }
    response = requests.request(method=method, url=url, json=params, headers=headers)
    try:
        return response.json()
    except requests.exceptions:
        return None
