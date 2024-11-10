from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


init_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Для чего этот бот?"),
     KeyboardButton(text="Регистрация"),
     KeyboardButton(text="Уже есть аккаунт")
     ]], resize_keyborad=True)

gender = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"),
     KeyboardButton(text="Женщина")]
], resize_keyboard=True)

