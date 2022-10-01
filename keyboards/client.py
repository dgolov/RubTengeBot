from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_expand = KeyboardButton('/Ввод_расходов')
button_menu = KeyboardButton('/Меню')

client_keyboard.add(button_expand).add(button_menu)
