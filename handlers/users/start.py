from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp


@dp.message_handler(Command("start"))
async def bot_start(message: types.Message):
    await message.answer(f" {message.from_user.full_name}, здравствуйте.")


@dp.message_handler(Command("search"))
async def bot_start(message: types.Message):
    await message.answer(f" {message.from_user.full_name}, введите номер телефона, какой хотите проверить.")
