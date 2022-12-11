import os
from peewee import SqliteDatabase, Model, PrimaryKeyField, IntegerField, CharField, DateField

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'test.db')
my_db = SqliteDatabase(db_path)


class BaseModel(Model):
    class Meta:
        database = my_db
        order_by = 'id'


class History(BaseModel):
    id = PrimaryKeyField(unique=True, null=False, primary_key=True)
    user_telegram_id = IntegerField(unique=True)
    time_request = DateField(null=True)
    city_name = CharField(null=True)
    hotels_name = CharField(null=True)


def create_db() -> None:
    """
    Функция создает базу данных, если она отсутствует.
    :return:
    """
    with open(db_path, 'w'):
        History.create_table()


if __name__ == '__main__':
    create_db()
