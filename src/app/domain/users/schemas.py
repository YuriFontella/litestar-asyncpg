from __future__ import annotations

from typing import Optional

from msgspec import Struct


class UserBase(Struct, kw_only=True, omit_defaults=True):
    """Base user schema with common fields."""

    name: str
    email: str
    role: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


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
