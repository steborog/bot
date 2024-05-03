from models.users_handler_models import PhoneData


def is_phone_number_valid(phone_number: str):
    return phone_number.startswith("+") and phone_number[1:-1].isnumeric() and len(phone_number) == 13


def build_phone_data_line(phone_data: PhoneData) -> str:
    return f"Користувач {phone_data.phone_number} {phone_data.name}"
