import os
from peewee import SqliteDatabase, Model, PrimaryKeyField, IntegerField, CharField, DateTimeField, BooleanField

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'test.db')
my_db = SqliteDatabase(db_path)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True, null=False, primary_key=True)
    user_telegram_id = IntegerField()

    class Meta:
        database = my_db
        order_by = 'id'


class History(BaseModel):
    time_request = DateTimeField()
    command_name = CharField()
    hotels_name = CharField()


class User(BaseModel):
    property_id = IntegerField(null=True)
    command = CharField(null=True)
    region_id = IntegerField(null=True)
    photos_status = BooleanField(null=True)
    number_of_photos = IntegerField(null=True)
    min_price = IntegerField(null=True)
    max_price = IntegerField(null=True)
    distance_from_center = CharField(null=True)
    arrival_date = CharField(null=True)
    departure_date = CharField(null=True)
    hotels_number_to_show = IntegerField(null=True)


def create_db() -> None:
    """
    Функция создает базу данных, если она отсутствует.
    :return:
    """
    with my_db:
        History.create_table()
        User.create_table()
        print("Готово")


if __name__ == '__main__':
    create_db()
