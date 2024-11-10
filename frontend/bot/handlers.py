import bot.keyboard as keyboards
import bot.text_answers as answers

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile

router = Router()


@router.message(CommandStart())
async def command_start(message: Message):
    await message.answer(text=answers.hello_message, reply_markup=keyboards.init_markup)


@router.message(Command('help'))
@router.message(F.text == 'Для чего этот бот?')
async def about(message: Message):
    print("hello")
    await message.answer(text=answers.about)

# @router.message(Command('register'))
# @router.callback_query(F.data == 'register')
