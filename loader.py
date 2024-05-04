from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from filters.auth_filter import AuthFilter
from middlewares.auth_middleware import AuthMiddleware

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

dp.filters_factory.bind(AuthFilter)
dp.setup_middleware(AuthMiddleware())
