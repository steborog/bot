class PhoneData:
    id: int
    name: str
    phone_number: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class User:
    id: int
    username: str
    alias: str
    telegram_id: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

