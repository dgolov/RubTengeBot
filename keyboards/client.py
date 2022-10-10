from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
expand_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_expand = KeyboardButton('/Ввод_расходов')
button_menu = KeyboardButton('/Меню')

button_previous = KeyboardButton('/назад')
button_cancel = KeyboardButton('/отмена')

inline_categories = [
    InlineKeyboardButton(text='Продукты', callback_data='категория продукты'),
    InlineKeyboardButton(text='Кафе', callback_data='категория кафе'),
    InlineKeyboardButton(text='Алкоголь', callback_data='категория алкоголь'),
    InlineKeyboardButton(text='Сигареты', callback_data='категория сигареты'),
    InlineKeyboardButton(text='Здоровье', callback_data='категория здоровье'),
    InlineKeyboardButton(text='Спорт', callback_data='категория спорт'),
    InlineKeyboardButton(text='Транспорт', callback_data='категория транспорт'),
    InlineKeyboardButton(text='Одежда', callback_data='категория одежда'),
    InlineKeyboardButton(text='Связь', callback_data='категория связь'),
    InlineKeyboardButton(text='Аренда', callback_data='категория аренда'),
    InlineKeyboardButton(text='Товары для дома', callback_data='категория дом'),
    InlineKeyboardButton(text='Прочие расходы', callback_data='категория прочие'),
]


client_keyboard.add(button_expand).add(button_menu)
expand_keyboard.add(button_cancel)
inline_categories_keyboard = InlineKeyboardMarkup(row_width=2)

for category in inline_categories:
    inline_categories_keyboard.add(category)
