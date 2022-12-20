from typing import Dict


class User:
    all_users = dict()

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        User.add_user(user_id=user_id)

    @classmethod
    def get_default(cls, data: Dict) -> Dict:
        data["command"] = ""
        data["city"] = ""
        data["region_id"] = 0
        data["hotels_number_to_show"] = 0
        data["photos_uploaded"] = {"status": False, "number_of_photos": 0}
        data["min_price"] = 0
        data["max_price"] = 0
        data["distance_from_center"] = ""
        data["arrival_date"] = ""
        data["departure_date"] = ""
        return data

    @classmethod
    def add_user(cls, user_id):
        if user_id not in cls.all_users.keys():
            cls.all_users[user_id] = cls.get_default({})

    @classmethod
    def get_data_with_user(cls, user_id):
        if user_id not in cls.all_users.keys():
            cls.add_user(user_id)
        return cls.all_users[user_id]
