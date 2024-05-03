from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from data.db import database_connection
from loader import dp
from states.UserStates import UserStates
from utils.users_handler_utils import is_phone_number_valid, PhoneData, build_phone_data_line


@dp.message_handler(Command("start"))
async def bot_start(message: Message):
    await message.answer(f" {message.from_user.full_name}, доброго дня!")


@dp.message_handler(Command("search"))
async def bot_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.number)
    await message.answer(f" {message.from_user.full_name}, введіть номер телефону для перевірки.")


@dp.message_handler(state=UserStates.number)
async def search_by_number(message: Message, state: FSMContext):
    number = message.text
    number = number.replace(" ", "")
    if is_phone_number_valid(number):
        results: list[dict] = (
            database_connection.execute("SELECT * FROM phones WHERE \"phone_number\" = ?", [number]).fetchall())
        report: str
        if len(results) > 0:
            report = "\n".join(map(lambda result: build_phone_data_line(PhoneData(**result)), results))
        else:
            report = 'Нажаль, записів за Вашим запитом не було знайдено.'
        await state.reset_state()
        await message.answer(report)
    else:
        await message.answer("Невалідний номер телефону. Введіть номер телефону у форматі +380XXXXXXXXX.")
