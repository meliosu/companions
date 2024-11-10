from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

init_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Для чего этот бот?"),
     KeyboardButton(text="Регистрация"),
     KeyboardButton(text="Уже есть аккаунт")
     ]], resize_keyborad=True)
