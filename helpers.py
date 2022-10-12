import aiohttp
import datetime
import json
import os
import re

from random import choice
from config import db_engine, logger


async def get_exchange_rate():
    """ Запрос в API курса валют для получения текущего курса тенге к рублю """
    url = os.environ.get('EXCHANGE_RATE_URL')
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url, ssl=False) as response:
            logger.info(f"[get_exchange_rate] GET {url} - status code: {response.status}")
            exchange_rate = await response.text(encoding='utf-8')
            result_kz = json.loads(exchange_rate)['Valute']['KZT']
    return result_kz['Nominal'] / result_kz['Value']


async def get_rub_expand(message: str, save: bool = True) -> tuple:
    """ Конвертация тенге в рубли
    :param message: сообщение пользователя
    :param save: сохранение в бд. Если False, то будет только конвертация и будет выведено другое сообщение
    :return: сумма в рублях, в тенге и ответное сообщение от бота
    """
    try:
        exchange_rate = await get_exchange_rate()
        tng = get_sum_from_message(message)
        rub = round(tng / exchange_rate, 2)
    except ValueError as e:
        logger.error(f'[get_rub_expand] Error: {e}')
        return None, None, None

    rub_txt = 'рублей'
    if str(int(rub)).endswith('1'):
        rub_txt = 'рубль'
    elif str(int(rub))[-1] in ('2', '3', '4'):
        rub_txt = 'рубля'

    result_message = f'💵 Ты потратил {rub} {rub_txt} 💵' if save else f'💵 Это будет {rub} {rub_txt} 💵'
    return rub, tng, result_message


def get_sum_from_message(message: str) -> float:
    """ Получение суммы расходов из сообщения """
    is_break = False
    result_sum = ''
    for char in message:
        if char.isdigit() or char in (',', '.'):
            is_break = True
            result_sum += char
            continue
        elif char.isalpha() and is_break:
            break

    return float(result_sum)


def get_greeting():
    """ Приветствие (На случай если кто то захочет здороваться с ботом) """
    time = datetime.datetime.utcnow().hour + 6

    default_greetings = ['Привет', 'Здравствуй']

    if 0 < time < 6:
        default_greetings.extend(['Доброй ночи'])
    elif 6 < time < 10:
        default_greetings.extend(['Доброе утро'])
    elif time < 18:
        default_greetings.extend(["Добрый день"])
    else:
        default_greetings.extend(["Добрый вечер"])
    return choice(default_greetings)


async def mach_answer(message):
    """ Поиск дефолтных ответов """
    text = message.text.lower()
    name = message.from_user.first_name

    rub, tng, result = await get_rub_expand(message=text, save=False)
    if result:
        return result

    if re.match(r'(^|\s)(привет|здравствуй(|те)|добр(ое|ый) (день|вечер|устро)|хай|хэллоу)', text) or \
            any(smile in text for smile in ('👋', '🙋', '🤚', '✋', '🤝', '✌️')):
        greeting = get_greeting()
        if name:
            greeting += f', {name}'
        return greeting

    elif re.match(r'как (дел|жизнь|поживаешь|сам|живешь|ты)', text):
        answer = choice(db_engine.get_answer_list(type_answer='how_are_you'))
    else:
        answer = choice(db_engine.get_answer_list(type_answer='default'))

    return answer.text


def get_statistic_message(result):
    """ Формирование сообщения статистики """
    message = f"\n{result.get('total')['tng_sum']} тенге\n{result.get('total')['rub_sum']} рублей\n"
    message += "\n💰 💰 💰 💰 Категории:\n"
    if result['categories']:
        for category, sum_dict in result['categories'].items():
            message += f"\n{category}: {sum_dict['tng_sum']} тенге = {sum_dict['rub_sum']} руб"
    return message
