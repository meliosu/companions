from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot.ride_handler import router, RideCallback
from bot.handlers import stub, api
import bot.text_answers as answers
from run import bot


@router.callback_query(RideCallback.filter(F.purpose == "ride_together"))
async def send_ride_offer(callback: CallbackQuery, data: RideCallback):
    sender = stub.GetUser(api.GetUserRequest(user_id=data.sender_id))

    first_name = sender.first_name
    last_name = sender.last_name
    age = sender.age
    abouts = sender.about

    about = f"Анкета:{first_name} {last_name}\nВозраст: {age}\nО Себе: {abouts}"

    chat = callback.message.chat
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Согласиться", callback_data=RideCallback(sender_id=data.recipient_id,
                                                                             sender_username=chat.username,
                                                                             recipient_id=data.sender_id,
                                                                             purpose="ride_together_back",
                                                                             sender_ride=data.recipient_ride,
                                                                             recipient_ride=sender.ride).pack())]
    ])

    if hasattr(sender, "avatar"):
        await bot.send_photo(chat_id=data.recipient_id, photo=sender.avatar, text=answers.ride_offer + about, reply_markup=markup)
    else:
        await bot.send_message(chat_id=data.recipient_id, text=answers.ride_offer + about, reply_markup=markup)


@router.callback_query(RideCallback.filter(F.purpose == "ride_together_back"))
async def send_ride_offer_back(callback: CallbackQuery, data: RideCallback):
    beginning = "Поздравляем, Вы нашли попутчика в поездку!\n\nНапишите @"
    end = " , чтобы договориться о дальнейших деталях."

    await callback.message.answer(text=beginning + data.sender_username + end)
    await bot.send_message(chat_id=data.recipient_id, text=beginning + callback.message.chat.username + end)

    stub.DeleteRide(api.DeleteRideRequest(ride_id=data.sender_ride))
    stub.DeleteRide(api.DeleteRideRequest(ride_id=data.recipient_ride))

