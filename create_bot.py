import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
dp = Dispatcher(bot, storage=storage)
