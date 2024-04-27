from msgspec import Struct


class User(Struct):
    email: str
    password: str
