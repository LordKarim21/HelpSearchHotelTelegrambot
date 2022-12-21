from telebot.types import Message
from loader import bot
from database.user_data import get_history


@bot.message_handler(commands=['history'])
def command_history(message: Message) -> None:
    all_history_user = ''
    for history in get_history(message.from_user.id):
        all_history_user += history + '\n'

    bot.send_message(message.chat.id, all_history_user)
