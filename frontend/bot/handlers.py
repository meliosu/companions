from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import bot.keyboard as keyboards
import bot.text_answers as answers

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

users_on_register = {}

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=answers.hello_message, reply_markup=keyboards.init_markup)


@router.message(Command('help'))
@router.message(F.text == 'Для чего этот бот?')
async def about(message: Message):
    await message.answer(text=answers.about)


class Form(StatesGroup):
    first_name = State()
    # last_name = State()
    age = State()
    gender = State()
    about = State()
    avatar = State()


class User:
    first_name: str = "def"
    last_name: str = "def"
    age: int = 0
    gender: bool = False
    about: str = "def"
    avatar: str = "def"


@router.message(Command('register'))
@router.message(F.text == "Регистрация")
async def register(message: Message, state: FSMContext):
    users_on_register[message.chat.id] = User()

    await state.set_state(Form.first_name)
    await message.answer(answers.register_1)


@router.message(Form.first_name)
async def process_first_and_last_name(message: Message, state: FSMContext):
    answer = message.text.split(" ")

    if len(answer) != 2:
        await message.answer(text=answers.register_1_err)
        return

    setattr(users_on_register[message.chat.id], "first_name", answer[0])
    setattr(users_on_register[message.chat.id], "last_name", answer[1])

    await state.set_state(Form.age)
    await message.answer(text=answers.register_2)


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text.split(" ")

    if len(age) != 1 or not age[0].isdigit():
        await message.answer(text=answers.register_2_err)
        return

    setattr(users_on_register[message.chat.id], "age", int(age[0]))

    await state.set_state(Form.gender)
    await message.answer(text=answers.register_3, reply_markup=keyboards.gender)


@router.message(Form.gender, F.text.casefold() == "мужчина")
async def process_man(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id], "gender", False)

    await state.set_state(Form.about)
    await message.answer(text=answers.register_4, reply_markup=ReplyKeyboardRemove())


@router.message(Form.gender, F.text.casefold() == "женщина")
async def process_woman(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id], "gender", True)

    await state.set_state(Form.about)
    await message.answer(text=answers.register_4, reply_markup=ReplyKeyboardRemove())


@router.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id], "about", message.text)

    form = form_str(message.chat.id)

    await state.clear()
    await message.answer(text=answers.register_success + form)

    # TODO: fix photo downloading
    # await state.set_state(Form.avatar)
    # await message.answer(text="Отправьте свое фото, которое будет видно всем пользователям сервиса")

    await state.clear()


def form_str(usr_id) -> str:
    ret = ""

    first_name = users_on_register[usr_id].first_name
    last_name = users_on_register[usr_id].last_name
    age = users_on_register[usr_id].age
    abouts = users_on_register[usr_id].about

    ret += f"{first_name} {last_name} {age} \n{abouts}"

    return ret

# @router.message(Form.avatar)
# async def process_avatar(message: Message, state: FSMContext):
#     users_on_register[message.chat.id].avatar = message.photo
#     TODO: add function that sends form to the backend
#     file = download(file=message.photo[-1].file_id)
#     setattr(users_on_register[message.chat.id], "avatar", 'photos/image.png')
