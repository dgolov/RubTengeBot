import re
import datetime

from random import choice


answer_dict = {
    'how_are_you': [
        'Спасибо, хорошо!', "Все хорошо!", "Хорошо!", "У меня все хорошо! :)", "Отлично", "Все супер :)",
    ],
    'default': [
        'Я умею только переводить тенге в рубли.', 'Прости, я не пнимаю тебя.',
    ]
}


def get_rub_expand(message: str) -> tuple:
    """ Конвертация тенге в рубли """
    try:
        tng = get_sum_from_message(message)
        rub = round(tng / 7.45, 2)
    except ValueError:
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
    time = datetime.datetime.now().hour

    default_greetings = ['Привет!', 'Здравствуй!']

    if time < 10:
        default_greetings.extend(['Доброе утро!'])
    elif time < 18:
        default_greetings.extend(["Добрый день!"])
    else:
        default_greetings.extend(["Добрый вечер!"])
    return choice(default_greetings)


async def mach_answer(message):
    """ Поиск дефолтных ответов """
    text = message.text.lower()
    name = message.from_user.first_name

    rub, tng, result = get_rub_expand(message=text)
    if result:
        return result

    if re.match(r'(^|\s)(привет|здравствуй(|те)|добр(ое|ый) (день|вечер|устро)|хай|хэллоу)', text):
        greeting = get_greeting()
        if name:
            greeting += f', {name}'
        return greeting

    elif re.match(r'как (дел|жизнь|поживаешь|сам|живешь|ты)', text):
        return choice(answer_dict.get('how_are_you'))
    else:
        return choice(answer_dict.get('default'))
