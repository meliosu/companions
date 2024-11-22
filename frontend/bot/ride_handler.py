import json
from datetime import datetime, timezone

from aiogram import F

from bot.handlers import stub, api, api_grpc

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import bot.keyboard as keyboards
import bot.text_answers as answers

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()
rides_in_process = {}


class Ride(StatesGroup):
    start_point = State()
    end_point = State()
    start_period = State()
    end_period = State()


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
    rides_in_process[message.chat.id].start_point.CopyFrom(location)

    await state.set_state(Ride.start_period)
    await message.answer(text=answers.ride_start_period)


@router.message(Ride.start_period)
async def process_start_period(message: Message, state: FSMContext):
    try:
        res = message.text.split(":")
        date = datetime.now().replace(hour=int(res[0]), minute=int(res[1]), second=0, microsecond=0)
        setattr(rides_in_process[message.chat.id], "start_period", date)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    await state.set_state(Ride.end_period)
    await message.answer(text=answers.ride_end_period)


async def send_ride(message, ride):
    ride_owner = stub.GetUser(api.GetUserRequest(user_id=ride.user_id))
    start_time = ride.start_period.astimezone(timezone.utc)
    end_time = ride.end_period.astimezone(timezone.utc)

    first_name = ride_owner.first_name
    last_name = ride_owner.last_name
    age = ride_owner.age
    abouts = ride_owner.about

    about = f"Начало поездки: {start_time}\nКонец поездки: {end_time}\n\nАнкета:{first_name} {last_name}\nВозраст: {age}\nО Себе: {abouts}"

    if hasattr(ride_owner, "avatar"):
        await message.answer_photo(caption=about, photo=ride_owner.avatar, reply_markup=keyboards.ride_markup)
    else:
        await message.answer(text=about, reply_markup=keyboards.ride_markup)


@router.message(Ride.end_period)
async def process_end_period(message: Message, state: FSMContext):
    key = message.chat.id

    try:
        res = message.text.split(":")
        date = datetime.now().replace(hour=int(res[0]), minute=int(res[1]), second=0, microsecond=0)
        setattr(rides_in_process[key], "end_period", date)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    stub.CreateRide(api.CreateRideRequest(ride=rides_in_process[key]))

    await state.clear()
    await message.answer(text=answers.ride_success)

    similar_rides: list = stub.GetSimilarRides(api.GetSimilarRidesRequest(ride=rides_in_process[key]))
    rides_in_process.pop(key)

    if not similar_rides:
        await message.answer(text=answers.no_similar_rides_found, reply_markup=keyboards.no_similar_ride)
        return

    for ride in similar_rides:
        await send_ride(message, ride)

    await message.answer(text=answers.all_rides_listed)