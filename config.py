import os
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from engine import EngineSessionFactory
from dotenv import load_dotenv


load_dotenv()


log_config = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": '%(asctime)s - %(levelname)s - %(message)s',
            "datefmt": '%d-%b-%y %H:%M:%S',
        },
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "formatter",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "formatter": "formatter",
            "filename": os.environ.get("LOGGING_PATH", None)
        },
    },
    "loggers": {
        "log": {
            "handlers": ["file_handler"],
            "level": "DEBUG",
        },
        "console": {
            "handlers": ["console_handler"],
            "level": "DEBUG",
        }
    },
}


logging.config.dictConfig(log_config)
logger_mode = 'console' if os.environ.get('DEBUG') else 'log'
logger = logging.getLogger(logger_mode)


db_engine = EngineSessionFactory(os.environ.get('DB_URL'))
storage = MemoryStorage()
bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
dp = Dispatcher(bot, storage=storage)
