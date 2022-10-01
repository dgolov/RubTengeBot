from aiogram import types, Dispatcher
from keyboards import client_keyboard


async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я бот учета рассходов в Казахстане. Введи ссумму в тенге и я переведу ее в рубли.",
        reply_markup=client_keyboard
    )


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start', 'help'])
