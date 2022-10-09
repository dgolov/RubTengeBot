import pytest

from patterns import *


@pytest.mark.parametrize('message,expected', [
    ('Я потратил 7450 тенге', 7450),
    ('Я потратил 1000 тенге', 1000),
    ('Я потратил 1000', 1000),
    ('1000 тенге', 1000),
    ('1000', 1000),
])
def test_get_sum_from_message(message, expected):
    result = get_sum_from_message(message)
    assert result == expected


def test_error_get_sum_from_message():
    with pytest.raises(ValueError):
        get_sum_from_message('Hello World')


@pytest.mark.parametrize('message,expected', [
    ('Я потратил 7450 тенге', (1000.0, 7450, "Ты потратил 1000.0 рублей")),
    ('Я потратил 1000 тенге', (134.23, 1000, "Ты потратил 134.23 рублей")),
    ('Я потратил 1000', (134.23, 1000, "Ты потратил 134.23 рублей")),
    ('1000 тенге', (134.23, 1000, "Ты потратил 134.23 рублей")),
    ('1000', (134.23, 1000, "Ты потратил 134.23 рублей")),
    ('Hello World', "Укажи пожалуйста сумму в тенге"),
])
def test_get_rub_expand(message, expected):
    result = get_rub_expand(message)
    assert result == expected
