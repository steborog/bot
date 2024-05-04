from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message
from loader import dp
from states.UserStates import UserStates
from utils.users_handler_utils import is_phone_number_valid, PhoneData, build_phone_data_line, login_or_register, \
    get_data_by_phone


@dp.message_handler(Command("start"))
async def bot_start(message: Message):
    login_report = login_or_register(message.from_user.id, message.from_user.full_name, message.from_user.username)
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
        phone_data = get_data_by_phone(number)
        report: str
        if phone_data is not None:
            report = f"{phone_data.name} {phone_data.phone_number}"
        else:
            report = 'Нажаль, записів за Вашим запитом не було знайдено.'
        await state.reset_state()
        await message.answer(report)
    else:
        await message.answer("Невалідний номер телефону. Введіть номер телефону у форматі +380XXXXXXXXX.")
