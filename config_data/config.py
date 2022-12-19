import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
HOST_API = os.getenv('HOST_API')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('history', "История поиска отелей"),
    ('lowprice', "Самые дешёвые отели в городе"),
    ('highprice', "Самые дорогие отели в городе"),
    ('bestdeal', "Вывод отелей, наиболее подходящих по цене и расположению от центра"),
    ('settings', "Установка параметров поиска (язык, валюта)"),
)
