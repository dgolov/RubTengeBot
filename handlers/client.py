from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, db_engine
from keyboards import client_keyboard, expand_keyboard, inline_categories_keyboard
from logging_settings import logger
from patterns import get_rub_expand


class FSMExpend(StatesGroup):
    """ Bot states class """
    sum = State()
    category = State()


def check_reset(func):
    """ Декоратор для проверки сброса состояния """
    async def wrapper(message: types.Message, state: FSMContext):
        if any(command in message.text for command in ('Ввод_расходов', 'start', 'help')):
            await message.answer('Действие отменено', reply_markup=client_keyboard)
            return await reset_state(message, state)
        else:
            return await func(message, state)
    return wrapper


async def reset_state(message: types.Message, state: FSMContext):
    """ Сброс состояния при вооде команд с клавиатуры """
    if 'Ввод_расходов' in message.text:
        logger.debug(f'[client - reset_state] {message.from_user.username} - reset set_expend')
        await state.finish()
        return await set_expense(message)
    else:
        logger.debug(f'[client - reset_state] {message.from_user.username} - reset send_welcome')
        await state.finish()
        return await send_welcome(message)


# --- HANDLERS ---


async def send_welcome(message: types.Message):
    """ Welcome and help message """
    user = db_engine.get_user_by_telegram_id(message.from_user.id)
    if not user:
        db_engine.create_new_user(message)

    logger.info(
        f'[client - send_welcome] {message.from_user.id} - {message.from_user.username} - message: {message.text}'
    )
    await message.reply(
        "Привет 👋\nЯ бот учета рассходов в Казахстане. Введи ссумму в тенге и я переведу ее в рубли."
        "\nЛибо воспользуйся командами с клавиатуры для более удобного взаимодействия. 👇👇👇"
        "\n🇰🇿 Алға Қазақстан! 🇰🇿",
        reply_markup=client_keyboard
    )


async def set_expense(message: types.Message):
    """ Convert rub to tng. State set sum """
    logger.info(f'[client - set_expense] {message.from_user.username} - message: {message.text}')
    await FSMExpend.sum.set()
    await message.answer('Введи сумму в тенге', reply_markup=expand_keyboard)


async def cancel_handler(message: types.Message, state: FSMContext):
    """ Cancel current state """
    logger.debug(f'[client - cancel_handler] {message.from_user.username} - cancel handler')
    current_state = await state.get_state()
    logger.debug(f'[client - cancel_state] {message.from_user.username} - current_state - {current_state}')
    if current_state is None:
        return
    await state.finish()
    await message.answer("Действие отменено", reply_markup=client_keyboard)


@check_reset
async def convert_expense(message: types.Message, state: FSMContext):
    """ Convert rub to tng. State convert """
    logger.info(f'[client - convert_expense] {message.from_user.username} - message: {message.text}')
    move_on = True
    rub, tng, answer = get_rub_expand(message.text)
    if not answer:
        logger.warning('[client - set_expense] {message.from_user.username} - convert exception')
        move_on = False
        answer = 'Ошибка конвертации. Похоже ты не указал сумму.'
    await message.answer(answer)
    if move_on:
        async with state.proxy() as data:
            data[message.from_user.id] = {}
            data[message.from_user.id]['sum'] = rub
        await FSMExpend.next()
        await message.answer("На что ты потратил эти деньги?", reply_markup=inline_categories_keyboard)


@check_reset
async def set_category(message: types.Message, state: FSMContext):
    """ Convert rub to tng. State set category """
    logger.info(f'[client - set_category] {message.from_user.username} - message: {message.text}')
    async with state.proxy() as data:
        data[message.from_user.id]['category'] = message.text
    await state.finish()
    await message.answer("Внесено в базу твоих расходов", reply_markup=client_keyboard)


@dp.callback_query_handler(Text(startswith='категория'), state=FSMExpend.category)
async def set_category_call(callback: types.CallbackQuery, state: FSMContext):
    logger.info(f'[client - set_category] {callback.from_user.username} - message: {callback.data}')
    async with state.proxy() as data:
        data[callback.from_user.id]['category'] = callback.data
    await state.finish()
    await callback.message.answer('Внесено в базу твоих расходов', reply_markup=client_keyboard)


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start', 'help'])
    dispatcher.register_message_handler(set_expense, commands=['Ввод_расходов'], state=None)
    dispatcher.register_message_handler(cancel_handler, commands=['cancel', 'отмена'], state='*')
    dispatcher.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dispatcher.register_message_handler(set_expense, Text(equals='ввести расход', ignore_case=True), state=None)
    dispatcher.register_message_handler(convert_expense, state=FSMExpend.sum)
    dispatcher.register_message_handler(set_category, state=FSMExpend.category)
