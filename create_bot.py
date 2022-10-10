import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from engine import EngineSessionFactory
from dotenv import load_dotenv


load_dotenv()

db_engine = EngineSessionFactory(os.environ.get('DB_URL'))
storage = MemoryStorage()
bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
dp = Dispatcher(bot, storage=storage)
