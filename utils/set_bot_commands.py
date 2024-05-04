from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_bot_commands(dp: Dispatcher, commands: list[BotCommand]):
    await dp.bot.set_my_commands(commands=commands)
