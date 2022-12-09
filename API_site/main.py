from typing import Dict
import requests
from .settings import SiteSettings
from database.user_data import get_lang

site = SiteSettings()


def make_response(method: str, url: str, headers: dict, params: dict,
                   timeout: int, success=200):
    response = requests.request(
        method=method, url=url, headers=headers, params=params, timeout=timeout
    )

    status_code = response.status_code
    if status_code == success:
        return response
    return status_code


def location_search(city: str, user_id: int,
                   timeout: int, func=make_response):
    method = "GET"
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    headers = {
        "X-RapidAPI-Key": site.app_key.get_secret_value(),
        "X-RapidAPI-Host": site.host_key
    }
    params = {
        'q': city, 'locale': get_lang(user_id)
    }
    response = func(method, url, headers, params, timeout)
    return response


def hotels_search(params: Dict, timeout: int, func=make_response):
    method = "POST"
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": site.app_key.get_secret_value(),
        "X-RapidAPI-Host": site.host_key
    }

    response = func(method, url, headers, params, timeout)
    return response


def photos_search(hotel_id: int, timeout: int, func=make_response):
    method = "GET"
    url = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
    headers = {
        "X-RapidAPI-Key": site.app_key.get_secret_value(),
        "X-RapidAPI-Host": site.host_key
    }
    params = {"id": "{}".format(hotel_id)}
    response = func(method, url, headers, params, timeout)
    return response
