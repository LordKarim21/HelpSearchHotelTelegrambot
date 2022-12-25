from typing import Dict
from telebot.types import Message
from config_data.contact_information import User


def get_data(message: Message) -> Dict:
    data = User.get_data_with_user(message.from_user.id)
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": data['property_id']
    }
    return payload
