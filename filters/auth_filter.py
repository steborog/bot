from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message


class AuthFilter(BoundFilter):
    async def check(self, message: Message):
        data = ctx_data.get()
        return data["current_user"] is not None
