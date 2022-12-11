import os
from peewee import SqliteDatabase, Model, PrimaryKeyField, IntegerField, CharField, ForeignKeyField, DateField

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'test.db')
my_db = SqliteDatabase(db_path)


class BaseModel(Model):
    id = PrimaryKeyField(unique=True, null=False, primary_key=True)

    class Meta:
        database = my_db
        order_by = 'id'


class UserData(BaseModel):
    user_telegram_id = IntegerField(unique=True)
    user_command = CharField(default='')
    #  Язык и валюта
    lang = CharField(default='')
    current = CharField(default='')
    #  rooms:
    adults = IntegerField(null=True)
    children = CharField(null=True)
    # city and hotel
    city_name = CharField(null=True)
    city_id = IntegerField(null=True)
    hotels_name = CharField(null=True)
    hotel_id = IntegerField(null=True)
    regionId = IntegerField(null=True)
    # date
    in_date = CharField(null=True)
    out_date = CharField(null=True)


class History(BaseModel):
    user = ForeignKeyField(UserData.user_telegram_id)
    time_request = DateField(null=True)
    hotel_name = CharField(null=True)


def create_db() -> None:
    """
    Функция создает базу данных, если она отсутствует.
    :return:
    """
    with my_db:
        UserData.create_table()
        History.create_table()


def creat_file() -> None:
    """
    Функция создает файл.
    :return:
    """
    with open(db_path, 'w'):
        pass


if __name__ == '__main__':
    creat_file()
    create_db()
