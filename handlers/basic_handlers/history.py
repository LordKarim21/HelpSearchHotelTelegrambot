from telebot.types import Message
from loader import bot
from database.user_data import get_history, clear_history


@bot.message_handler(commands=['history'])
def command_history(message: Message) -> None:
    all_history_user = "\n".join([history for history in get_history(message.from_user.id)])
    if len(all_history_user) > 4095:
        for x in range(0, len(all_history_user), 4095):
            bot.send_message(message.from_user.id, text=all_history_user[x:x + 4094])
    else:
        bot.send_message(message.from_user.id, text=all_history_user)


@bot.message_handler(commands=['clear_history'])
def command_clear_history(message: Message) -> None:
    clear_history(message.from_user.id)
    bot.send_message(message.chat.id, "История очистилась")
