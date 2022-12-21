from telebot.types import Message
from config_data.contact_information import User
from loader import bot
from keyboards.inline.position import get_inline_buttons_position


def get_hotel_num(message: Message) -> None:
    if message.text.isdigit():
        keyboard = get_inline_buttons_position()
        bot.send_message(message.from_user.id,
                         "Спасибо, записал. Вам показать фотографий отелей?", reply_markup=keyboard)
        data = User.get_data_with_user(message.from_user.id)
        data['hotels_number_to_show'] = int(message.text) if int(message.text) != 0 else 5
    else:
        bot.send_message(message.from_user.id, "Количесто фотографий дожно быть числом")
