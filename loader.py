from typing import Dict

from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from telebot.types import Message

from config_data import config

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
