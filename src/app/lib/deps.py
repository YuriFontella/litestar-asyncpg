from __future__ import annotations

from typing import Any

from litestar.connection import ASGIConnection


def provide_current_user(connection: ASGIConnection) -> Any | None:
    """Fornece o usuário autenticado atual extraído do objeto de conexão."""
    return connection.user if hasattr(connection, "user") else None
