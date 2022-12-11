from typing import Dict
from config_data import config
import requests


def make_response(method: str, url: str, headers: dict, params: dict, timeout: int = 10, success=200):
    response = requests.request(
        method=method, url=url, headers=headers, params=params, timeout=timeout
    )
    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def location_search(city: str,  timeout: int = None, func=make_response):
    method = "GET"
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }
    params = {
        'q': city, 'locale': "en_US", "langid": "1033", "siteid": "300000001"
    }
    if timeout is None:
        response = func(method=method, url=url, headers=headers, params=params)
    else:
        response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)
    return response


def hotels_search(params: Dict, timeout: int, func=make_response):
    method = "POST"
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }

    # payload = {
    #     "currency": "USD",
    #     "eapid": 1,
    #     "locale": "en_US",
    #     "siteId": 300000001,
    #     "destination": {"regionId": "6054439"},
    #     "checkInDate": {
    #         "day": 10,
    #         "month": 10,
    #         "year": 2022
    #     },
    #     "checkOutDate": {
    #         "day": 15,
    #         "month": 10,
    #         "year": 2022
    #     },
    #     "rooms": [
    #         {
    #             "adults": 2,
    #             "children": [{"age": 5}, {"age": 7}]
    #         }
    #     ],
    #     "resultsStartingIndex": 0,
    #     "resultsSize": 200,
    #     "sort": "PRICE_LOW_TO_HIGH",
    #     "filters": {"price": {
    #         "max": 150,
    #         "min": 100
    #     }}

    if timeout is None:
        response = func(method=method, url=url, headers=headers, params=params)
    else:
        response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)
    return response


def photos_search(params: Dict, timeout: int, func=make_response):
    method = "POST"
    url = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }
    # payload = {
    #     "currency": "USD",
    #     "eapid": 1,
    #     "locale": "en_US",
    #     "siteId": 300000001,
    #     "propertyId": "9209612"
    # }
    if timeout is None:
        response = func(method=method, url=url, headers=headers, params=params)
    else:
        response = func(method=method, url=url, headers=headers, params=params, timeout=timeout)
    return response
