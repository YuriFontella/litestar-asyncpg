from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from msgspec import Struct

from src.domain.entities.base import BaseEntity


class User(BaseEntity, kw_only=True):
    """Entidade de usuário."""
    id: Optional[int] = None
    name: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = True
    email: str
    password: str


class Session(BaseEntity, kw_only=True):
    """Entidade de sessão."""
    id: Optional[int] = None
    user_agent: Optional[str] = None
    ip: Optional[str] = None
    revoked: Optional[bool] = False
    date: Optional[datetime] = None
    access_token: str
    user_id: int


class Player(BaseEntity, kw_only=True):
    """Entidade de jogador."""
    id: Optional[int] = None
    team_id: Optional[int] = None
    language: Optional[str] = 'pt-br'
    uuid: Optional[str] = None
    status: Optional[bool] = False
    name: str


class Team(BaseEntity, kw_only=True):
    """Entidade de equipe."""
    id: Optional[int] = None
    date: Optional[datetime] = None
    players: Optional[List[Player]] = None
    name: str
    price: Decimal
    owner: str
    protocol: int


class Token(BaseEntity):
    """Entidade de token."""
    token: str