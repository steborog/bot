from typing import Optional

from data.db import database_connection
from models.users_handler_models import PhoneData
from models.users_handler_models import User
from data.config import PHONES_TABLE_NAME, USERS_TABLE_NAME


def is_phone_number_valid(phone_number: str):
    return phone_number.startswith("+") and phone_number[1:-1].isnumeric() and len(phone_number) == 13


def build_phone_data_line(phone_data: PhoneData) -> str:
    return f"Користувач {phone_data.phone_number} {phone_data.name}"


def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    user_dict = database_connection.execute(
        f"SELECT * FROM {USERS_TABLE_NAME} WHERE \"telegram_id\" = ?", [telegram_id]
    ).fetchone()

    if user_dict is not None:
        return User(**user_dict)
    else:
        return None


def login_or_register(telegram_id: int, alias: str, username: str) -> str:
    answer: str

    user = get_user_by_telegram_id(telegram_id)

    if user is not None:
        answer = f"Раді бачити Вас знову, {user.alias}!"
    else:
        database_connection.execute(
            f"INSERT INTO \"{USERS_TABLE_NAME}\" (telegram_id, alias, username) values (?,?,?)",
            [telegram_id, alias, username]
        )
        database_connection.commit()
        answer = f"Доброго дня, {alias}, Вас було успішно зареєстровано!"

    return answer


def get_data_by_phone(phone: str) -> Optional[PhoneData]:
    phone_data_dict = (database_connection.execute(f"SELECT * FROM {PHONES_TABLE_NAME} WHERE \"phone_number\" = ?",
                                        [phone]).fetchone())

    if phone_data_dict is not None:
        return PhoneData(**phone_data_dict)
    else:
        return None