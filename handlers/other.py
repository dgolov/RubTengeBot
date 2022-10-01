from aiogram import types, Dispatcher
from logging_settings import logger
from patterns import mach_answer, get_rub_expand


async def echo(message: types.Message):
    """ Отвечает на дефотлные сообщения """
    logger.info(f'{message.from_user.username} - message: {message.text}')
    answer = await mach_answer(message)
    await message.answer(answer)


async def set_expend(message: types.Message):
    """ Конвертирует тенге в рубли """
    logger.info(f'{message.from_user.username} - message: {message.text}')
    await message.reply(get_rub_expand(message.text))


def register_handlers_others(dispatcher: Dispatcher):
    dispatcher.register_message_handler(set_expend, commands=['Ввод_расходов'])
    dispatcher.register_message_handler(echo)
