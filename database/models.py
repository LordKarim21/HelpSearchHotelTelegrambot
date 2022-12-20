import os
from datetime import datetime
from peewee import SqliteDatabase, Model, PrimaryKeyField, IntegerField, CharField, DateField

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
    time_request = DateField(default=datetime.now)
    command_name = CharField(null=True)
    hotels_name = CharField(null=True)


def create_db() -> None:
    """
    Функция создает базу данных, если она отсутствует.
    :return:
    """
    with my_db:
        History.create_table()
        print("Готово")


if __name__ == '__main__':
    create_db()
