from aiogram import executor
from create_bot import dp
from logging_settings import console_logger, logger
from handlers import client, other


async def on_startup(_):
    console_logger.info("Bot is online")
    logger.info("Bot is online")


if __name__ == '__main__':
    client.register_handlers_client(dp)
    other.register_handlers_others(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
