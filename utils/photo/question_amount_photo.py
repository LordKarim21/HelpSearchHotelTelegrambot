from telebot.types import Message
from database.user_data import set_photos_status, set_number_of_photos
from loader import bot
from utils.response.get_response import response_hotels


def get_photo_amount(message: Message):
    if message.text.isdigit():
        set_photos_status(message.from_user.id, True)
        set_number_of_photos(message.from_user.id, int(message.text))
        response_hotels(message)
    else:
        answer = bot.send_message(message.from_user.id, "Количесто фотографий дожно быть числом")
        bot.register_next_step_handler(answer, get_photo_amount)
