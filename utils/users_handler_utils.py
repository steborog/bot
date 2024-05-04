from typing import Optional

from data.config import PHONES_TABLE_NAME, USERS_TABLE_NAME, USERS_SEARCH_RECORDS_TABLE_NAME
from data.db import database_connection
from loader import common_logger
from models.users_handler_models import PhoneData, SearchRecord
from models.users_handler_models import User


def is_phone_number_valid(phone_number: str):
    return phone_number.startswith("+") and phone_number[1:-1].isnumeric() and len(phone_number) == 13


def build_phone_data_line(phone_data: PhoneData) -> str:
    return f"Користувач {phone_data.phone_number} {phone_data.name}"


def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    user_dict = database_connection.execute(
        f"SELECT * FROM {USERS_TABLE_NAME} WHERE telegram_id = ?", [telegram_id]
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
        common_logger.info(f"Зареєстрований новий користувач: telegram id - {telegram_id}, username: {username},"
                           f"alias: {alias}")
        database_connection.execute(
            f"INSERT INTO \"{USERS_TABLE_NAME}\" (telegram_id, alias, username) values (?,?,?)",
            [telegram_id, alias, username]
        )
        database_connection.commit()
        answer = f"Доброго дня, {alias}, Вас було успішно зареєстровано!"

    return answer


def get_data_by_phone(phone: str) -> Optional[PhoneData]:
    phone_data_dict = (database_connection.execute(f"SELECT * FROM {PHONES_TABLE_NAME} WHERE phone_number = ?",
                                                   [phone]).fetchone())

    if phone_data_dict is not None:
        return PhoneData(**phone_data_dict)
    else:
        return None


def write_search_record(user_id: int, input: str):
    database_connection.execute(f"INSERT INTO {USERS_SEARCH_RECORDS_TABLE_NAME} (user_id, query) VALUES (?, ?)",
                                [user_id, input])
    database_connection.commit()


def get_user_queries(user_id: int) -> list[SearchRecord]:
    results = database_connection.execute(f"SELECT * FROM {USERS_SEARCH_RECORDS_TABLE_NAME} WHERE user_id = ?"
                                          "ORDER BY id DESC",
                                          [user_id]).fetchall()
    return list(map(lambda result_dict: SearchRecord(**result_dict), results))


def build_query_report(record: SearchRecord):
    return f"{record.id}: {record.query}"
