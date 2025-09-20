from __future__ import annotations
from msgspec import Struct


"""Data Transfer Objects (DTOs) for request/response serialization."""


# Response wrapper for consistent API responses
class APIResponse(Struct):
    """Standard API response wrapper."""

    success: bool = True
    message: str = ""
    data: dict | list | None = None
