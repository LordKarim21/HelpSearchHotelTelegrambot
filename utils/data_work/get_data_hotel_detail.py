from typing import Dict
from telebot.types import Message
from config_data.contact_information import User


def get_data(property_id: int) -> Dict:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": str(property_id)
    }
    return payload
