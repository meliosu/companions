from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


init_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Для чего этот бот?"),
     KeyboardButton(text="Регистрация"),
     KeyboardButton(text="Уже есть аккаунт")
     ]], resize_keyborad=True)

default_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Моя анкета"),
     KeyboardButton(text="Создать заявку")]
], resize_keyboard=True)

gender = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"),
     KeyboardButton(text="Женщина")]
], resize_keyboard=True)

