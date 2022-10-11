import re
import datetime

from random import choice
from config import db_engine, logger


def get_rub_expand(message: str) -> tuple:
    """ Конвертация тенге в рубли """
    try:
        tng = get_sum_from_message(message)
        rub = round(tng / 7.45, 2)
    except ValueError as e:
        logger.error(f'[get_rub_expand] Error: {e}')
        return None, None, None

    rub_txt = 'рублей'
    if str(int(rub)).endswith('1'):
        rub_txt = 'рубль'
    elif str(int(rub))[-1] in ('2', '3', '4'):
        rub_txt = 'рубля'

    return rub, tng, f'Ты потратил {rub} {rub_txt}'


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

    rub, tng, result = get_rub_expand(message=text)
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
