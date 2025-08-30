from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UserRegisterIn:
    name: str
    email: str
    password: str


@dataclass(slots=True)
class UserAuthIn:
    email: str
    password: str

