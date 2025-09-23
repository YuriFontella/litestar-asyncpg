from __future__ import annotations

from typing import Dict, Callable, Any, TypeAlias

from litestar import Request
from litestar.stores.registry import StoreRegistry

# Tipo específico para a função emit da aplicação
EventEmitter: TypeAlias = Callable[[str, Any], None]


def provide_current_user(request: Request) -> Dict | None:
    """Fornece o usuário autenticado atual extraído do objeto de autenticação."""
    return request.user if hasattr(request, "user") else None


def provide_stores(request: Request) -> StoreRegistry:
    """Fornece o registry de stores da aplicação."""
    return request.app.stores


def provide_emit(request: Request) -> EventEmitter:
    """Fornece a função emit da aplicação para emitir eventos."""
    return request.app.emit
