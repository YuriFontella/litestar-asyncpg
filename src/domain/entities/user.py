from __future__ import annotations

from typing import Optional
from msgspec import Struct


class User(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = None
    status: Optional[bool] = None


class AuthCredentials(Struct):
    email: str
    password: str

