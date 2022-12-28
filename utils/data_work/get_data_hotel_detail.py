from typing import Dict


def get_data(property_id: int) -> Dict:
    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": str(property_id)
    }
    return payload
