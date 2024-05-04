from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from data import config
from data.commands import commands
from data.loggers import common_logger
from filters.auth_filter import AuthFilter
from middlewares.auth_middleware import AuthMiddleware

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

bot.set_my_commands(commands=commands.values())
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

dp.filters_factory.bind(AuthFilter)
dp.setup_middleware(AuthMiddleware())
dp.setup_middleware(LoggingMiddleware(
    common_logger.name
))
