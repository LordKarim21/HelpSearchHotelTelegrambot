from typing import Dict
from telebot.types import Message
from config_data.contact_information import User


def get_data(message: Message):
    user = User.get_data_with_user(message.from_user.id)
    params = {
        "currency": user['currency'],
        "eapid": 1,
        "locale": user["language"],
        "siteId": 300000001,
        "propertyId": "9209612"
    }
    return params
