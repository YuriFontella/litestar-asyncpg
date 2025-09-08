from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from msgspec import Struct


class Team(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    price: Decimal
    owner: Optional[str] = None
    protocol: Optional[int] = None
    date: Optional[datetime] = None


class Player(Struct, kw_only=True, omit_defaults=True):
    id: Optional[int] = None
    name: str
    language: Optional[str] = None
    uuid: Optional[str] = None
    status: Optional[bool] = None
    team_id: Optional[int] = None


class TeamWithPlayers(Team):
    players: List[Player]

