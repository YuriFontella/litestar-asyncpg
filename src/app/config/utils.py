from __future__ import annotations

import os
from typing import TypeVar

T = TypeVar("T")


def get_env(key: str, default: T) -> T:
    """Get environment variable with default value.

    Args:
        key: Environment variable name
        default: Default value if env var not found

    Returns:
        Environment variable value or default
    """
    value = os.getenv(key)
    if value is None:
        return default

    # Handle boolean conversion
    if isinstance(default, bool):
        return value.lower() in ("true", "1", "yes", "on")  # type: ignore

    # Handle int conversion
    if isinstance(default, int):
        return int(value)  # type: ignore

    # Handle list conversion (comma-separated string)
    if isinstance(default, list):
        return [item.strip() for item in value.split(",")]  # type: ignore

    # Return as string for everything else
    return value  # type: ignore
