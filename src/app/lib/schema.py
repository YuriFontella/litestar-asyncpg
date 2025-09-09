from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from msgspec import Struct


class User(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: Optional[str] = None
    email: str
    password: str
    role: Optional[str] = None
    status: Optional[bool] = None


class Teams(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    price: Decimal
    owner: Optional[str] = None
    protocol: Optional[int] = None
    date: Optional[datetime] = None


class Players(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    language: Optional[str] = None
    uuid: Optional[str] = None
    status: Optional[bool] = None
    team_id: Optional[int] = None


class TeamsPlayers(Teams):
    players: list[Players]


class Token(Struct):
    token: str
