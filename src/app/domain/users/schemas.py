from __future__ import annotations

from typing import Optional
from datetime import datetime

from msgspec import Struct


class UserBase(Struct, kw_only=True, omit_defaults=True):
    """Base user schema with common fields."""

    name: str
    email: str
    role: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(Struct, kw_only=True, omit_defaults=True):
    """Schema for updating user information."""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    status: Optional[bool] = None


class UserRead(UserBase):
    """Schema for reading user data (excludes password)."""

    id: int
    status: bool


class User(Struct, kw_only=True, omit_defaults=True):
    """Full user schema for internal operations."""

    id: Optional[int] = None
    name: str
    email: str
    password: str
    role: Optional[str] = None
    status: Optional[bool] = None


class UserLogin(Struct):
    """Schema for user login."""

    email: str
    password: str


class Token(Struct):
    """JWT token response."""

    token: str
    type: str = "Bearer"


class SessionBase(Struct, kw_only=True):
    """Base session schema."""

    user_agent: Optional[str] = None
    ip: Optional[str] = None
    user_id: int


class SessionCreate(SessionBase):
    """Schema for creating a session."""

    access_token: str


class SessionRead(SessionBase):
    """Schema for reading session data."""

    id: int
    access_token: str
    revoked: bool
    date: datetime
