from telebot.types import Message
from database.user_data import set_hotels_number_to_show
from loader import bot
from keyboards.inline.position import get_inline_buttons_position


def get_hotel_num(message: Message) -> None:
    if message.text.isdigit():
        keyboard = get_inline_buttons_position()
        bot.send_message(message.from_user.id,
                         "Спасибо, записал. Вам показать фотографий отелей?", reply_markup=keyboard)
        hotels_number_to_show = int(message.text) if int(message.text) != 0 else 5
        set_hotels_number_to_show(message.from_user.id, hotels_number_to_show)
    else:
        answer = bot.send_message(message.from_user.id, "Количесто фотографий дожно быть числом")
        bot.register_next_step_handler(answer, get_hotel_num)
