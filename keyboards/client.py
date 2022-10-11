from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import db_engine


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
expand_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
statistic_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

button_expand = KeyboardButton('/Ввод_расходов')
button_menu = KeyboardButton('/Статистика')

button_previous = KeyboardButton('/назад')
button_cancel = KeyboardButton('/отмена')


button_statistic_all = KeyboardButton('/За_все_время')
button_statistic_month = KeyboardButton('/За_месяц')
button_statistic_week = KeyboardButton('/За_неделю')
button_statistic_day = KeyboardButton('/За_сегодня')

categories = db_engine.get_all_categories()

inline_categories = []

for category in categories:
    inline_categories.append(InlineKeyboardButton(text=category.name, callback_data=category.slug))

client_keyboard.add(button_expand).add(button_menu)
expand_keyboard.add(button_cancel)
statistic_keyboard.insert(button_statistic_all).insert(button_statistic_month).insert(button_statistic_week).\
    insert(button_statistic_day).add(button_cancel)

inline_categories_keyboard = InlineKeyboardMarkup(row_width=2)

for category in inline_categories:
    inline_categories_keyboard.add(category)
