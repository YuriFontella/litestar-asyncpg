from __future__ import annotations

from typing import Dict, Callable, Any, TypeAlias

from litestar import Request
from litestar.stores.registry import StoreRegistry

# Specific type for the application's emit function
EventEmitter: TypeAlias = Callable[[str, Any], None]


def provide_current_user(request: Request) -> Dict | None:
    """Provides the current authenticated user extracted from the authentication object."""
    return request.user if hasattr(request, "user") else None


def provide_stores(request: Request) -> StoreRegistry:
    """Provides the application's store registry."""
    return request.app.stores


def provide_emit(request: Request) -> EventEmitter:
    """Provides the application's emit function for emitting events."""
    return request.app.emit
