import json
from datetime import datetime, timezone

from aiogram import F
from aiogram.filters.callback_data import CallbackData

from bot.handlers import stub, api, api_grpc

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import bot.keyboard as keyboards
import bot.text_answers as answers

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()
rides_in_process = {}


class Ride(StatesGroup):
    start_point = State()
    end_point = State()
    start_period = State()
    end_period = State()


class RideCallback(CallbackData, prefix="ride"):
    sender_id: int
    sender_username: str
    recipient_id: int
    purpose: str
    sender_ride: int
    recipient_ride: int


@router.message(F.text == "Создать заявку")
async def ride_creation_start(message: Message, state: FSMContext):
    key = message.chat.id
    if key in rides_in_process:
        await message.answer(text=answers.cannot_create_more_than_one_ride_simultaneously)
        return

    rides_in_process[key] = api.Ride(user_id=key)

    await state.set_state(Ride.start_point)
    await message.answer(text=answers.ride_start_point)


@router.message(Ride.start_point)
async def process_start_point(message: Message, state: FSMContext):
    # TODO: Implement point search by text

    if not message.location:
        await message.answer(text=answers.no_location_provided)
        return

    location = api.Location(latitude=message.location.latitude, longitude=message.location.longitude)
    rides_in_process[message.chat.id].start_point.CopyFrom(location)

    await state.set_state(Ride.end_point)
    await message.answer(text=answers.ride_end_point)


@router.message(Ride.end_point)
async def process_start_point(message: Message, state: FSMContext):
    # TODO: Implement point search by text

    if not message.location:
        await message.answer(text=answers.no_location_provided)
        return

    location = api.Location(latitude=message.location.latitude, longitude=message.location.longitude)
    rides_in_process[message.chat.id].end_point.CopyFrom(location)

    await state.set_state(Ride.start_period)
    await message.answer(text=answers.ride_start_period)


@router.message(Ride.start_period)
async def process_start_period(message: Message, state: FSMContext):
    try:
        res = message.text.split(":")
        date = datetime.now().replace(hour=int(res[0]), minute=int(res[1]), second=0, microsecond=0)
        date_now = datetime.now()
        
        

        setattr(rides_in_process[message.chat.id], "start_period", date)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    await state.set_state(Ride.end_period)
    await message.answer(text=answers.ride_end_period)


async def send_ride(message, ride, ride_response):
    ride_owner = stub.GetUser(api.GetUserRequest(user_id=ride.user_id))

    print(ride.start_period)

    start_time = datetime.fromtimestamp(ride.start_period.seconds).strftime("%d/%m %I:%M:%S")
    end_time = datetime.fromtimestamp(ride.end_period.seconds).strftime("%d/%m %I:%M:%S")

    first_name = ride_owner.first_name
    last_name = ride_owner.last_name
    age = ride_owner.age
    abouts = ride_owner.about

    about = f"Начало поездки: {start_time} \nКонец поездки: {end_time} \n\nАнкета:{first_name} {last_name}\nВозраст: {age}\nО Себе: {abouts}"

    ride_together = RideCallback(sender_id=message.chat.id, sender_username=message.chat.username,
                                 recipient_id=ride.user_id, purpose="ride_together",
                                 sender_ride=ride.id, recipient_ride=ride_response.ride_id)
    decline = RideCallback(sender_id=message.chat.id, sender_username=message.chat.username,
                           recipient_id=ride.user_id, purpose="decline_ride",
                           sender_ride=ride.id, recipient_ride=ride_response.ride_id)
    block_user = RideCallback(sender_id=message.chat.id, sender_username=message.chat.username,
                              recipient_id=ride.user_id, purpose="block_user",
                              sender_ride=ride.id, recipient_ride=ride_response.ride_id)

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Поехать вместе", callback_data=ride_together.pack())],
         [InlineKeyboardButton(text="Отклонить", callback_data=decline.pack())],
         [InlineKeyboardButton(text="Заблокировать", callback_data=block_user.pack())]
    ])

    if hasattr(ride_owner, "avatar"):
        await message.answer_photo(caption=about, photo=ride_owner.avatar, reply_markup=markup)
    else:
        await message.answer(text=about, reply_markup=keyboards.ride_markup)


@router.message(Ride.end_period)
async def process_end_period(message: Message, state: FSMContext):
    key = message.chat.id

    try:
        res = message.text.split(":")
        date = datetime.now().replace(hour=int(res[0]), minute=int(res[1]), second=0, microsecond=0)
        date_now = datetime.now()

        if date_now > date:
            await message.answer(text="Это время уже прошло. Пожалуйста, введите время корректно.")
            return

        setattr(rides_in_process[key], "end_period", date)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    ride_response: api.CreateRideResponse = stub.CreateRide(api.CreateRideRequest(ride=rides_in_process[key]))
    setattr(rides_in_process[message.chat.id], "id", ride_response.ride_id)

    await state.clear()
    await message.answer(text=answers.ride_success)

    similar_rides = stub.GetSimilarRides(api.GetSimilarRidesRequest(ride=rides_in_process[key],
                                                                    start_radius=200, end_radius=200))

    rides_in_process.pop(key)

    if not similar_rides.rides:
        await message.answer(text=answers.no_similar_rides_found, reply_markup=keyboards.no_similar_ride)
        return

    for ride in similar_rides.rides:
        await send_ride(message, ride, ride_response)

    await message.answer(text=answers.all_rides_listed)


@router.callback_query(F.data == "wait_for_companion")
async def process_wait_for_companion(callback: CallbackQuery):
    await callback.message.answer(text=answers.wait_for_companion)


@router.callback_query(F.data == "delete_ride")
async def process_ride_deletion(callback: CallbackQuery):
    stub.DeleteRide(api.DeleteRideRequest(ride_id=rides_in_process[callback.message.chat.id].id))
    rides_in_process.pop(callback.message.chat.id)

    await callback.message.answer(text=answers.ride_deleted_after_no_similar)


@router.callback_query(RideCallback.filter(F.purpose == "decline_ride"))
async def process_ride_decline(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(RideCallback.filter(F.purpose == "block_user"))
async def process_user_block(callback: CallbackQuery, data: RideCallback):
    stub.BlockUser(api.BlockUserRequest(blocking_user_id=data.sender_id, blocked_user_id=data.recipient_id))

    await callback.message.delete()


@router.callback_query(RideCallback.filter(F.purpose == "ride_together"))
async def send_ride_offer(callback: CallbackQuery, callback_data: RideCallback):
    sender = stub.GetUser(api.GetUserRequest(user_id=callback_data.sender_id))

    first_name = sender.first_name
    last_name = sender.last_name
    age = sender.age
    abouts = sender.about

    about = f"Анкета:{first_name} {last_name}\nВозраст: {age}\nО Себе: {abouts}"

    chat = callback.message.chat
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Согласиться", callback_data=RideCallback(sender_id=callback_data.recipient_id,
                                                                             sender_username=chat.username,
                                                                             recipient_id=callback_data.sender_id,
                                                                             purpose="ride_together_back",
                                                                             sender_ride=callback_data.recipient_ride,
                                                                             recipient_ride=0).pack()),
         InlineKeyboardButton(text="Отклонить", callback_data=RideCallback(sender_id=callback_data.recipient_id,
                                                                           sender_username=chat.username,
                                                                           recipient_id=callback_data.sender_id,
                                                                           purpose="decline_ride_back",
                                                                           sender_ride=callback_data.recipient_ride,
                                                                           recipient_ride=0).pack()),
         InlineKeyboardButton(text="Заблокировать", callback_data=RideCallback(sender_id=callback_data.recipient_id,
                                                                               sender_username=chat.username,
                                                                               recipient_id=callback_data.sender_id,
                                                                               purpose="block_user_back",
                                                                               sender_ride=callback_data.recipient_ride,
                                                                               recipient_ride=0).pack())]
    ])

    if hasattr(sender, "avatar"):
        await callback.message.bot.send_photo(chat_id=callback_data.recipient_id, photo=sender.avatar, caption=answers.ride_offer + about,
                             reply_markup=markup)
    else:
        await callback.message.bot.send_message(chat_id=callback_data.recipient_id, text=answers.ride_offer + about, reply_markup=markup)


@router.callback_query(RideCallback.filter(F.purpose == "ride_together_back"))
async def send_ride_offer_back(callback: CallbackQuery, callback_data: RideCallback):
    beginning = "Поздравляем, Вы нашли попутчика в поездку!\n\nНапишите @"
    end = " , чтобы договориться о дальнейших деталях."

    await callback.message.answer(text=beginning + callback_data.sender_username + end)
    await callback.message.bot.send_message(chat_id=callback_data.recipient_id, text=beginning + callback.message.chat.username + end)

    stub.DeleteRide(api.DeleteRideRequest(ride_id=callback_data.sender_ride))
    stub.DeleteRide(api.DeleteRideRequest(ride_id=callback_data.recipient_ride))


@router.callback_query(RideCallback.filter(F.purpose == "decline_ride_back"))
async def send_ride_decline_back(callback: CallbackQuery, callback_data: RideCallback):
    await callback.message.bot.send_message(chat_id=callback_data.recipient_id, text=answers.ride_declined)


@router.callback_query(RideCallback.filter(F.purpose == "block_user_back"))
async def send_ride_decline_back(callback: CallbackQuery, callback_data: RideCallback):
    stub.BlockUser(api.BlockUserRequest(blocking_user_id=callback_data.sender_id, blocked_user_id=callback_data.recipient_id))

    await callback.message.answer(text=answers.user_blocked)


@router.message(CommandStart())
async def start_cmd(message: Message):
    """Handle /start command"""
    await message.answer(
        text=answers.hello_message,
        reply_markup=keyboards.init_markup
    )

@router.message(Command("help"))
async def help_cmd(message: Message):
    """Handle /help command"""
    await message.answer(
        text=answers.about,
        reply_markup=keyboards.init_markup
    )

@router.message(F.text == "⚙️ Настройки")
async def settings(message: Message):
    """Handle settings menu"""
    settings_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить анкету", callback_data="edit_profile")],
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications")],
        [InlineKeyboardButton(text="❌ Удалить аккаунт", callback_data="delete_account")]
    ])
    await message.answer("⚙️ Настройки:", reply_markup=settings_markup)
