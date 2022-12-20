from telebot.types import Message
from config_data.contact_information import User
from loader import bot


def get_hotel_num(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Спасибо, записал. Вам показать фотографий отелей?")
        data = User.get_data_with_user(message.from_user.id)
        data['hotels_number_to_show'] = int(message.text) if int(message.text) != 0 else 5
    else:
        bot.send_message(message.from_user.id, "Количесто фотографий дожно быть числом")
