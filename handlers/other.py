from aiogram import types, Dispatcher
from config import dp, logger
from helpers import mach_answer


async def echo(message: types.Message):
    """ Отвечает на дефотлные сообщения """
    logger.info(f'[echo] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    answer = await mach_answer(message)
    await message.answer(answer)


@dp.message_handler(lambda message: 'такси' in message.text)
async def taxi(message: types.Message):
    """ Get taxi phone """
    logger.info(f'[taxi] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    await message.answer('Такси Дастар (Капчагай): +77277240500')


def register_handlers_others(dispatcher: Dispatcher):
    dispatcher.register_message_handler(echo)
