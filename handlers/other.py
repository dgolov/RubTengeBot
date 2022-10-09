from aiogram import types, Dispatcher
from logging_settings import logger
from patterns import mach_answer


async def echo(message: types.Message):
    """ Отвечает на дефотлные сообщения """
    logger.info(f'[other - echo] {message.from_user.username} - message: {message.text}')
    answer = await mach_answer(message)
    await message.answer(answer)


def register_handlers_others(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo)
