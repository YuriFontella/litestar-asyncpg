from typing import Optional
from datetime import datetime
from decimal import Decimal
from msgspec import Struct


class User(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    email: str
    password: str
    role: Optional[str] = None
    status: Optional[bool] = None


class Players(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    user: Optional[str] = None
    language: Optional[str] = None
    uuid: Optional[str] = None
    status: Optional[bool] = None


class Teams(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    value: Decimal
    player_id: Optional[int] = None
    protocol: Optional[int] = None
    date: Optional[datetime] = None
