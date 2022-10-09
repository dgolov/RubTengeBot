from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
expand_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_expand = KeyboardButton('/Ввод_расходов')
button_menu = KeyboardButton('/Меню')

button_previous = KeyboardButton('/назад')
button_cancel = KeyboardButton('/отмена')

client_keyboard.add(button_expand).add(button_menu)
expand_keyboard.add(button_cancel)
