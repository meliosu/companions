from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


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

no_similar_ride = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Дождаться", callback_data="wait_for_companion"),
     InlineKeyboardButton(text="Удалить", callback_data="delete_ride")]
])

ride_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Поехать вместе", callback_data="share_ride"),
     InlineKeyboardButton(text="Отклонить", callback_data="decline_ride"),
     InlineKeyboardButton(text="Заблокировать", callback_data="block_user")]
])

