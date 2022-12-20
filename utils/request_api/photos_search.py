from typing import Dict
from requests import Response, request
from config_data import config


def photos_search(params: Dict, timeout: int = None) -> Response:
    method = "POST"
    url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }
    if timeout is None:
        time = 10
    else:
        time = timeout
    response = request(method=method, url=url, headers=headers, params=params, timeout=time)
    return response.json()
