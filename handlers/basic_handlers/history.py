from telebot.types import Message
from loader import bot
from database.user_data import get_history


@bot.message_handler(commands=['history'])
def command_history(message: Message) -> None:
    bot.send_message(message.chat.id, get_history(message.from_user.id))
