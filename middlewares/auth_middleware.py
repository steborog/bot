from typing import Optional

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from models.users_handler_models import User
from utils.users_handler_utils import get_user_by_telegram_id


class AuthMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        telegram_id = message.from_user.id
        user: Optional[User] = get_user_by_telegram_id(telegram_id)
        data["current_user"] = user
