from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from msgspec import Struct
from src.app.config.base import get_settings


class PlayerBase(Struct, kw_only=True, omit_defaults=True):
    """Base player schema."""

    name: str
    # Use dynamic default from settings so it can be overridden via env.
    language: Optional[str] = get_settings().app.DEFAULT_PLAYER_LANGUAGE


class PlayerCreate(PlayerBase):
    """Schema for creating a player."""

    pass


class PlayerRead(PlayerBase):
    """Schema for reading player data."""

    id: int
    uuid: str
    status: bool
    team_id: int


class TeamBase(Struct, kw_only=True, omit_defaults=True):
    """Base team schema."""

    name: str
    price: Decimal
    owner: str


class TeamRead(TeamBase):
    """Schema for reading team data."""

    id: int
    protocol: int
    date: datetime


class Team(Struct, kw_only=True, omit_defaults=True):
    """Full team schema for internal operations."""

    id: Optional[int] = None
    name: str
    price: Decimal
    owner: str
    protocol: Optional[int] = None
    date: Optional[datetime] = None


class TeamWithPlayersCreate(TeamBase):
    """Schema for creating a team with players."""

    players: list[PlayerCreate]


class TeamWithPlayersRead(TeamRead):
    """Schema for reading team with players."""

    players: list[PlayerRead]
