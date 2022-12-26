from typing import Dict


class User:
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        User.add_user(user_id=user_id)

    @classmethod
    def get_default(cls) -> Dict:
        data = {
            "property_id": "",
            "command": "",
            "city": "",
            "region_id": 0,
            "photos_uploaded": {"status": False, "number_of_photos": 5},
            "min_price": 0,
            "max_price": 0,
            "distance_from_center": "",
            "arrival_date": "",
            "departure_date": ""
        }
        return data

    @classmethod
    def add_user(cls, user_id):
        if user_id not in cls.all_users.keys():
            cls.all_users[user_id] = cls.get_default()

    @classmethod
    def get_data_with_user(cls, user_id):
        if user_id not in cls.all_users.keys():
            cls.add_user(user_id)
        return cls.all_users[user_id]
