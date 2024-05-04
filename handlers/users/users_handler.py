from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message

from filters.auth_filter import AuthFilter
from loader import dp
from models.users_handler_models import User, SearchRecord
from states.UserStates import UserStates
from utils.users_handler_utils import is_phone_number_valid, PhoneData, build_phone_data_line, login_or_register, \
    get_data_by_phone, write_search_record, get_user_queries, build_query_report


@dp.message_handler(Command("start"))
async def bot_start(message: Message):
    login_report = login_or_register(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(login_report)


@dp.message_handler(AuthFilter(), Command("search"))
async def bot_start(message: Message, state: FSMContext, current_user: User):
    await state.set_state(UserStates.number)
    await message.answer(f" {current_user.alias}, введіть номер телефону для перевірки.")


@dp.message_handler(AuthFilter(), state=UserStates.number)
async def search_by_number(message: Message, state: FSMContext, current_user: User):
    number = message.text
    number = number.replace(" ", "")
    if is_phone_number_valid(number):
        phone_data = get_data_by_phone(number)
        write_search_record(current_user.id, message.text)
        report: str
        if phone_data is not None:
            report = f"{phone_data.name} {phone_data.phone_number}"
        else:
            report = 'Нажаль, записів за Вашим запитом не було знайдено.'
        await state.reset_state()
        await message.answer(report)
    else:
        await message.answer("Невалідний номер телефону. Введіть номер телефону у форматі +380XXXXXXXXX.")


@dp.message_handler(AuthFilter(), Command('history'))
async def list_queries_history(message: Message, current_user: User):
    queries: list[SearchRecord] = get_user_queries(current_user.id)

    report: str
    if len(queries) > 0:
        report = "Ось список Ваших запитів:\n" + "\n".join(map(build_query_report, queries))
    else:
        report = "За Вашим обліковим записом не знайдено жодних запитів"

    await message.answer(report)