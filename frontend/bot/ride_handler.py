from datetime import datetime, timezone

from aiogram import F
from google.protobuf.internal.well_known_types import Timestamp

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

    setattr(rides_in_process[message.chat.id], "start_point", location)

    await state.set_state(Ride.end_point)
    await message.answer(text=answers.ride_end_point)


@router.message(Ride.end_point)
async def process_start_point(message: Message, state: FSMContext):
    # TODO: Implement point search by text

    if not message.location:
        await message.answer(text=answers.no_location_provided)
        return

    location = api.Location(latitude=message.location.latitude, longitude=message.location.longitude)
    setattr(rides_in_process[message.chat.id], "end_point", location)

    await state.set_state(Ride.start_period)
    await message.answer(text=answers.ride_end_point)


@router.message(Ride.start_period)
async def process_start_period(message: Message, state: FSMContext):
    try:
        res = message.text.split(":")
        print(res[0], res[1])
        date = datetime(year=message.date.year, month=message.date.month, day=message.date.day, hour=int(res[0]),
                        minute=int(res[1]), second=0)
        date.replace(tzinfo=timezone.utc)

        timestamp = Timestamp()
        timestamp.FromDatetime(date)

        setattr(rides_in_process[message.chat.id], "start_period", timestamp)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    await state.set_state(Ride.end_period)
    await message.answer(text=answers.ride_end_period)


@router.message(Ride.end_period)
async def process_end_period(message: Message, state: FSMContext):
    key = message.chat.id

    try:
        res= message.text.split(":")
        date = datetime(year=message.date.year, month=message.date.month, day=message.date.day, hour=int(res[0]),
                        minute=int(res[1]), second=0)

        timestamp = Timestamp()
        timestamp.FromDatetime(date)

        setattr(rides_in_process[key], "end_period", timestamp)
    except ValueError:
        await message.answer(text=answers.bad_time)
        return

    # stub.CreateRide(api.CreateRideRequest(ride=rides_in_process[key]))
    rides_in_process.pop(key)

    await state.clear()
    await message.answer(text=answers.ride_success)
