from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from msgspec import Struct
from src.app.config.constants import DEFAULT_PLAYER_LANGUAGE


class PlayerBase(Struct, kw_only=True, omit_defaults=True):
    """Base player schema."""

    name: str
    language: Optional[str] = DEFAULT_PLAYER_LANGUAGE


class PlayerCreate(PlayerBase):
    """Schema for creating a player."""

    pass


class PlayerUpdate(Struct, kw_only=True, omit_defaults=True):
    """Schema for updating a player."""

    name: Optional[str] = None
    language: Optional[str] = None
    status: Optional[bool] = None


class PlayerRead(PlayerBase):
    """Schema for reading player data."""

    id: int
    uuid: str
    status: bool
    team_id: int


class Player(Struct, kw_only=True, omit_defaults=True):
    """Full player schema for internal operations."""

    id: Optional[int] = None
    name: str
    language: Optional[str] = DEFAULT_PLAYER_LANGUAGE
    uuid: Optional[str] = None
    status: Optional[bool] = False
    team_id: Optional[int] = None


class TeamBase(Struct, kw_only=True, omit_defaults=True):
    """Base team schema."""

    name: str
    price: Decimal
    owner: str


class TeamCreate(TeamBase):
    """Schema for creating a team."""

    pass


class TeamUpdate(Struct, kw_only=True, omit_defaults=True):
    """Schema for updating a team."""

    name: Optional[str] = None
    price: Optional[Decimal] = None
    owner: Optional[str] = None


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


# Backward compatibility aliases
Teams = Team
Players = Player
TeamsPlayers = TeamWithPlayersRead
