from config_data import config
import requests


def location_search(city: str, locale: str = "en_US",  timeout: int = None):
    method = "GET"
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    headers = {
        "X-RapidAPI-Key": config.RAPID_API_KEY,
        "X-RapidAPI-Host": config.HOST_API
    }
    params = {
        'q': city, 'locale': locale
    }
    timeout = 20 if timeout is None else timeout
    response = requests.request(
        method=method, url=url, headers=headers, params=params, timeout=timeout
    )
    return response
