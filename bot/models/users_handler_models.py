class BaseModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class PhoneData(BaseModel):
    id: int
    name: str
    phone_number: str


class User(BaseModel):
    id: int
    username: str
    alias: str
    telegram_id: str


class SearchRecord(BaseModel):
    id: int
    user_id: int
    query: str
