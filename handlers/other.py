from aiogram import types, Dispatcher
from create_bot import dp
from logging_settings import logger
from patterns import mach_answer


async def echo(message: types.Message):
    """ Отвечает на дефотлные сообщения """
    logger.info(f'[other - echo] {message.from_user.username} - message: {message.text}')
    answer = await mach_answer(message)
    await message.answer(answer)


@dp.message_handler(lambda message: 'такси' in message.text)
async def taxi(message: types.Message):
    """ Get taxi phone """
    logger.info(f'[other - taxi] {message.from_user.username} - message: {message.text}')
    await message.answer('Такси Дастар (Капчагай): +77277240500')


def register_handlers_others(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo)
