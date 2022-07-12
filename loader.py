from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from data import BOT_TOKEN

storage = MemoryStorage()
bot = Bot(BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot, storage=storage)