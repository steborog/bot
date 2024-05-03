from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from data.config import PHONES_TABLE_NAME, USERS_TABLE_NAME
from data.db import database_connection
from loader import dp
from models.users_handler_models import User
from states.UserStates import UserStates
from utils.users_handler_utils import is_phone_number_valid, PhoneData, build_phone_data_line


def loginOrRegister(telegram_id: int, alias: str, username: str) -> str:
    search_list = database_connection.execute(
        f"SELECT * FROM {USERS_TABLE_NAME} WHERE \"telegram_id\" = ?", [telegram_id]
    ).fetchall()

    answer: str

    if len(search_list) > 0:
        existed_user = User(**search_list[0])
        answer = f"Раді бачити Вас знову, {existed_user.alias}!"
    else:
        database_connection.execute(
            f"INSERT INTO \"{USERS_TABLE_NAME}\" (telegram_id, alias, username) values (?,?,?)", [telegram_id, alias, username]
        )
        answer = f"Доброго дня, {alias}, Вас було успішно зареєстровано!"

    return answer


@dp.message_handler(Command("start"))
async def bot_start(message: Message):
    login_report = loginOrRegister(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(login_report)


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
            database_connection.execute(f"SELECT * FROM {PHONES_TABLE_NAME} WHERE \"phone_number\" = ?",
                                        [number]).fetchone())
        report: str
        if len(results) > 0:
            report = "\n".join(map(lambda result: build_phone_data_line(PhoneData(**result)), results))
        else:
            report = 'Нажаль, записів за Вашим запитом не було знайдено.'
        await state.reset_state()
        await message.answer(report)
    else:
        await message.answer("Невалідний номер телефону. Введіть номер телефону у форматі +380XXXXXXXXX.")
