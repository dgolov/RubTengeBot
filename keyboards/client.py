from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import db_engine


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
expand_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_expand = KeyboardButton('/Ввод_расходов')
button_menu = KeyboardButton('/Меню')

button_previous = KeyboardButton('/назад')
button_cancel = KeyboardButton('/отмена')

categories = db_engine.get_all_categories()

inline_categories = []

for category in categories:
    inline_categories.append(
        InlineKeyboardButton(text=category.name, callback_data=f'категория {category.name.lower()}')
    )


client_keyboard.add(button_expand).add(button_menu)
expand_keyboard.add(button_cancel)
inline_categories_keyboard = InlineKeyboardMarkup(row_width=2)

for category in inline_categories:
    inline_categories_keyboard.add(category)
