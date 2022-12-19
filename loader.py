from typing import Dict

from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot.types import Message

from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)


def save_data(message: Message, data_items: Dict) -> None:
    storage.save(message.chat.id, message.from_user.id, data_items)
