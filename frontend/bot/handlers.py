import os

import grpc
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import bot.keyboard as keyboards
import bot.text_answers as answers

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

import rpc.api_pb2_grpc as api_grpc
import rpc.api_pb2 as api

users_on_register = {}

router = Router()
channel = grpc.insecure_channel(os.environ['COMPANIONS_BACKEND_ADDRESS'])
stub = api_grpc.CompanionsStub(channel)


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=answers.hello_message, reply_markup=keyboards.init_markup)


@router.message(F.text == "Моя анкета")
@router.message(F.text == "Уже есть аккаунт")
async def print_user_form(message: Message):
    try:
        usr = stub.GetUser(api.GetUserRequest(user_id=message.chat.id))
    except Exception as e:
        await message.answer(text="Кажется, в нашей базе нет Вашей анкеты. Пожалуйста, зарегистрируйтесь!")
        return
    

    form = form_str(usr)

    if hasattr(usr, "avatar"):
        await message.reply_photo(photo=usr.avatar, caption=form, reply_markup=keyboards.default_markup);
    else:
        await message.answer(text=form, reply_markup=keyboards.default_markup)


@router.message(F.text == "Редактировать анкету")
async def change_form(message: Message, state: FSMContext):
    users_on_register[message.chat.id] = {}
    users_on_register[message.chat.id][0] = api.User(id=message.chat.id)
    users_on_register[message.chat.id][1] = 1;

    await state.set_state(Form.first_name)
    await message.answer(answers.register_1)



@router.message(Command('help'))
@router.message(F.text == "О боте")
async def about(message: Message):
    await message.answer(text=answers.about)


class Form(StatesGroup):
    first_name = State()
    age = State()
    gender = State()
    about = State()
    avatar = State()


@router.message(Command('register'))
@router.message(F.text == "👤 Регистрация")
async def register(message: Message, state: FSMContext):
    users_on_register[message.chat.id] = {}
    users_on_register[message.chat.id][0] = api.User(id=message.chat.id)
    users_on_register[message.chat.id][1] = 0;

    await state.set_state(Form.first_name)
    await message.answer(answers.register_1)


@router.message(Form.first_name)
async def process_first_and_last_name(message: Message, state: FSMContext):
    answer = message.text.split(" ")

    if len(answer) != 2:
        await message.answer(text=answers.register_1_err)
        return

    setattr(users_on_register[message.chat.id][0], "first_name", answer[0])
    setattr(users_on_register[message.chat.id][0], "last_name", answer[1])

    await state.set_state(Form.age)
    await message.answer(text=answers.register_2)


@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    age = message.text.split(" ")

    if len(age) != 1 or not age[0].isdigit():
        await message.answer(text=answers.register_2_err)
        return

    setattr(users_on_register[message.chat.id][0], "age", int(age[0]))

    await state.set_state(Form.gender)
    await message.answer(text=answers.register_3, reply_markup=keyboards.gender)


@router.message(Form.gender, F.text.casefold() == "мужчина")
async def process_man(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id][0], "gender", api.Gender.MALE)

    await state.set_state(Form.about)
    await message.answer(text=answers.register_4, reply_markup=ReplyKeyboardRemove())


@router.message(Form.gender, F.text.casefold() == "женщина")
async def process_woman(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id][0], "gender", api.Gender.FEMALE)

    await state.set_state(Form.about)
    await message.answer(text=answers.register_4, reply_markup=ReplyKeyboardRemove())


@router.message(Form.about)
async def process_about(message: Message, state: FSMContext):
    setattr(users_on_register[message.chat.id][0], "about", message.text)

    await state.set_state(Form.avatar)
    await message.answer(text=answers.register_5)


def form_str(usr) -> str:
    ret = ""

    first_name = usr.first_name
    last_name = usr.last_name
    age = usr.age
    abouts = usr.about

    ret += f"{first_name} {last_name}\nВозраст: {age}\nО Себе: {abouts}"

    return ret


@router.message(Form.avatar)
async def process_avatar(message: Message, state: FSMContext):
    usr = users_on_register[message.chat.id][0]
    form = form_str(usr)

    if not message.photo:
        if users_on_register[message.chat.id][1] == 0:
            stub.CreateUser(api.CreateUserRequest(user=usr))
        else:
            stub.DeleteUser(api.DeleteUserRequest(user_id=message.chat.id))
            stub.CreateUser(api.CreateUserRequest(user=usr))
        users_on_register.pop(message.chat.id)

        await state.clear()
        await message.answer(text=answers.register_success + form, reply_markup=keyboards.default_markup)
        return

    setattr(usr, "avatar", message.photo[-1].file_id)

    if users_on_register[message.chat.id][1] == 0:
        stub.CreateUser(api.CreateUserRequest(user=usr))
    else:
        stub.DeleteUser(api.DeleteUserRequest(user_id=message.chat.id))
        stub.CreateUser(api.CreateUserRequest(user=usr))

    form = form_str(usr)

    users_on_register.pop(message.chat.id)

    await state.clear()
    await message.answer_photo(caption=answers.register_success + form, photo=message.photo[-1].file_id,
                               reply_markup=keyboards.default_markup)



