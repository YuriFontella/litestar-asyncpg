from __future__ import annotations

from typing import Dict

from litestar import Request


def provide_current_user(request: Request) -> Dict | None:
    """Fornece o usuário autenticado atual extraído do objeto de autenticação."""
    return request.user if hasattr(request, "user") else None
