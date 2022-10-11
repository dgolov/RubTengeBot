from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from config import dp, db_engine, logger
from helpers import get_rub_expand, get_statistic_message
from keyboards import client_keyboard, expand_keyboard, inline_categories_keyboard, statistic_keyboard

from datetime import datetime, timedelta

from handlers.states import FSMExpend, FSMStatistic


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
    if any(command in message.text for command in ('Ввод_расходов', 'Статистика')):
        logger.debug(f'[reset_state] {message.from_user.id} - {message.from_user.username} - reset set_expend')
        await state.finish()
        return await set_expense(message)
    else:
        logger.debug(f'[reset_state] {message.from_user.id} - {message.from_user.username} - reset send_welcome')
        await state.finish()
        return await send_welcome(message)


# --- HANDLERS ---


async def send_welcome(message: types.Message):
    """ Welcome and help message """
    user = db_engine.get_user_by_telegram_id(message.from_user.id)
    if not user:
        db_engine.create_new_user(message)

    logger.info(f'[send_welcome] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    await message.reply(
        "Привет 👋\nЯ бот учета рассходов в Казахстане. Введи ссумму в тенге и я переведу ее в рубли."
        "\nЛибо воспользуйся командами с клавиатуры для более удобного взаимодействия. 👇👇👇"
        "\n🇰🇿 Алға Қазақстан! 🇰🇿",
        reply_markup=client_keyboard
    )


async def set_expense(message: types.Message):
    """ Convert rub to tng. State set sum """
    logger.info(f'[set_expense] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    await FSMExpend.sum.set()
    await message.answer('Введи сумму в тенге', reply_markup=expand_keyboard)


async def cancel_handler(message: types.Message, state: FSMContext):
    """ Cancel current state """
    logger.debug(f'[client - cancel_handler] {message.from_user.id} - {message.from_user.username} - cancel handler')
    current_state = await state.get_state()
    logger.debug(
        f'[cancel_state] {message.from_user.id} - {message.from_user.username} - current_state - {current_state}'
    )
    if current_state is None:
        return
    await state.finish()
    await message.answer("Действие отменено", reply_markup=client_keyboard)


@check_reset
async def convert_expense(message: types.Message, state: FSMContext):
    """ Convert rub to tng. State convert """
    logger.info(f'[convert_expense] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    move_on = True
    rub, tng, answer = get_rub_expand(message.text)
    if not answer:
        logger.warning(f'[set_expense] {message.from_user.id} - {message.from_user.username} - convert exception')
        move_on = False
        answer = 'Ошибка конвертации. Похоже ты не указал сумму.'
    await message.answer(answer)
    if move_on:
        async with state.proxy() as data:
            data[message.from_user.id] = {}
            data[message.from_user.id]['sum_rub'] = rub
            data[message.from_user.id]['sum_tng'] = tng
        await FSMExpend.next()
        await message.answer("На что ты потратил эти деньги?", reply_markup=inline_categories_keyboard)


@check_reset
async def set_category(message: types.Message, state: FSMContext):
    """ Convert rub to tng. State set category """
    logger.info(f'[set_category] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    async with state.proxy() as data:
        data[message.from_user.id]['category'] = message.text
    await state.finish()
    try:
        await set_cost(message.from_user.id, data[message.from_user.id])
        await message.answer("✅ Внесено в базу твоих расходов ✅", reply_markup=client_keyboard)
    except Exception as e:
        logger.info(f'[set_category_call] {message.from_user.id} - {message.from_user.username} - Error: {e}')
        await message.answer('Ошибка внесения расходов в базу данных... Сорян(', reply_markup=client_keyboard)


@dp.callback_query_handler(Text(startswith='category'), state=FSMExpend.category)
async def set_category_call(callback: types.CallbackQuery, state: FSMContext):
    """ Convert rub to tng. State set category callback """
    logger.info(
        f'[set_category_call] {callback.from_user.id} - {callback.from_user.username} - message: {callback.data}'
    )
    async with state.proxy() as data:
        data[callback.from_user.id]['category'] = callback.data
    await state.finish()
    try:
        await set_cost(callback.from_user.id, data[callback.from_user.id])
        await callback.message.answer('Внесено в базу твоих расходов', reply_markup=client_keyboard)
    except Exception as e:
        logger.info(f'[set_category_call] {callback.from_user.id} - {callback.from_user.username} - Error: {e}')
        await callback.message.answer('Ошибка внесения расходов в базу данных... Сорян(', reply_markup=client_keyboard)


async def set_cost(user_id, data):
    """ Save storage to database """
    try:
        db_engine.set_cost(user_id, data)
        logger.info(f'[set_cost] {user_id} - data saved successfully')
    except Exception as e:
        logger.info(f'[set_cost] {user_id} - data saved failed. Error: {e}')


async def get_statistic(message: types.Message):
    """ Получение статистики расходов. Переключение на состояние выбора периода """
    logger.info(f'[get_statistic] {message.from_user.id} - {message.from_user.username} - message: {message.text}')
    await FSMStatistic.start.set()
    await message.answer(f"Укажи период", reply_markup=statistic_keyboard)


async def set_all_statistic_period(message: types.Message, state=FSMStatistic.start):
    """ Получение всей статистики """
    logger.info(
        f'[set_all_statistic_period] {message.from_user.id} - {message.from_user.username} - message: {message.text}'
    )
    result = db_engine.get_statistics(telegram_user_id=message.from_user.id)
    logger.debug(f'[set_all_statistic_period] {message.from_user.id} - statistic: {result}')
    await state.finish()
    await message.answer(
        f"За все время ты потратил: {get_statistic_message(result)}",
        reply_markup=client_keyboard
    )


async def set_month_statistic_period(message: types.Message, state=FSMStatistic.start):
    """ Получение статистики за месяц """
    logger.info(
        f'[set_month_statistic_period] {message.from_user.id} - {message.from_user.username} - message: {message.text}'
    )
    today = datetime.utcnow() + timedelta(hours=6)
    start = datetime.utcnow() + timedelta(hours=6) - timedelta(days=today.day - 1)
    period = {
        'start': start.date(),
        'end': today,
    }

    try:
        result = db_engine.get_statistics(telegram_user_id=message.from_user.id, period=period)
    except Exception as e:
        logger.error(f'[set_day_statistic_period] {message.from_user.id} - error: {e}')
        await message.answer(f"Ошибка получении статистики", reply_markup=client_keyboard)
    else:
        logger.debug(f'[set_month_statistic_period] {message.from_user.id} - statistic: {result}')
        await message.answer(
            f"За текуший месяц ты потратил: {get_statistic_message(result)}",
            reply_markup=client_keyboard
        )
    finally:
        await state.finish()


async def set_week_statistic_period(message: types.Message, state=FSMStatistic.start):
    """ Получение статистики за неделю """
    logger.info(
        f'[set_week_statistic_period] {message.from_user.id} - {message.from_user.username} - message: {message.text}'
    )
    today = datetime.utcnow() + timedelta(hours=6)
    start = datetime.utcnow() + timedelta(hours=6) - timedelta(days=today.weekday())
    period = {
        'start': start.date(),
        'end': today
    }

    try:
        result = db_engine.get_statistics(telegram_user_id=message.from_user.id, period=period)
    except Exception as e:
        logger.error(f'[set_day_statistic_period] {message.from_user.id} - error: {e}')
        await message.answer(f"Ошибка получении статистики", reply_markup=client_keyboard)
    else:
        logger.debug(f'[set_week_statistic_period] {message.from_user.id} - statistic: {result}')
        await message.answer(
            f"За текушую неделю ты потратил: {get_statistic_message(result)}",
            reply_markup=client_keyboard
        )
    finally:
        await state.finish()


async def set_today_statistic_period(message: types.Message, state=FSMStatistic.start):
    """ Получение статистики за сегодня """
    logger.info(
        f'[set_today_statistic_period] {message.from_user.id} - {message.from_user.username} - message: {message.text}'
    )
    today = datetime.utcnow() + timedelta(hours=6)
    period = {
        'start': today.date(),
        'end': today,
    }
    logger.debug(f'[set_today_statistic_period] {message.from_user.id} - period: {period}')
    try:
        result = db_engine.get_statistics(telegram_user_id=message.from_user.id, period=period)
    except Exception as e:
        logger.error(f'[set_today_statistic_period] {message.from_user.id} - error: {e}')
        await message.answer(f"Ошибка получении статистики", reply_markup=client_keyboard)
    else:
        logger.debug(f'[set_today_statistic_period] {message.from_user.id} - statistic: {result}')
        await message.answer(
            f"За текуший день ты потратил: {get_statistic_message(result)}",
            reply_markup=client_keyboard
        )
    finally:
        await state.finish()


async def set_yesterday_statistic_period(message: types.Message, state=FSMStatistic.start):
    """ Получение статистики за вчера """
    logger.info(
        f'[set_yesterday_statistic_period] {message.from_user.id} - {message.from_user.username} - '
        f'message: {message.text}'
    )
    today = datetime.utcnow() + timedelta(hours=6)
    start = today - timedelta(days=1)
    period = {
        'start': start.date(),
        'end': today,
    }

    logger.debug(f'[set_yesterday_statistic_period] {message.from_user.id} - period: {period}')
    try:
        result = db_engine.get_statistics(telegram_user_id=message.from_user.id, period=period)
    except Exception as e:
        logger.error(f'[set_yesterday_statistic_period] {message.from_user.id} - error: {e}')
        await message.answer(f"Ошибка получении статистики", reply_markup=client_keyboard)
    else:
        logger.debug(f'[set_yesterday_statistic_period] {message.from_user.id} - statistic: {result}')
        await message.answer(
            f"За вчерашниЙ день ты потратил: {get_statistic_message(result)}",
            reply_markup=client_keyboard
        )
    finally:
        await state.finish()


####################################################


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start', 'help'])
    dispatcher.register_message_handler(set_expense, commands=['Ввод_расходов'], state=None)
    dispatcher.register_message_handler(cancel_handler, commands=['cancel', 'отмена'], state='*')
    dispatcher.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    dispatcher.register_message_handler(set_expense, Text(equals='ввести расход', ignore_case=True), state=None)
    dispatcher.register_message_handler(convert_expense, state=FSMExpend.sum)
    dispatcher.register_message_handler(set_category, state=FSMExpend.category)
    dispatcher.register_message_handler(get_statistic, commands=['Статистика'], state=None)
    dispatcher.register_message_handler(set_all_statistic_period, commands=['За_все_время'], state=FSMStatistic.start)
    dispatcher.register_message_handler(
        set_all_statistic_period, Text(contains='все', ignore_case=True), state=FSMStatistic.start
    )
    dispatcher.register_message_handler(set_month_statistic_period, commands=['За_месяц'], state=FSMStatistic.start)
    dispatcher.register_message_handler(
        set_month_statistic_period, Text(contains='месяц', ignore_case=True), state=FSMStatistic.start
    )
    dispatcher.register_message_handler(set_week_statistic_period, commands=['За_неделю'], state=FSMStatistic.start)
    dispatcher.register_message_handler(
        set_week_statistic_period, Text(contains='недел', ignore_case=True), state=FSMStatistic.start
    )
    dispatcher.register_message_handler(set_today_statistic_period, commands=['За_сегодня'], state=FSMStatistic.start)
    dispatcher.register_message_handler(
        set_today_statistic_period, Text(contains='сегодня', ignore_case=True), state=FSMStatistic.start
    )
    dispatcher.register_message_handler(
        set_yesterday_statistic_period, Text(contains='вчера', ignore_case=True), state=FSMStatistic.start
    )
