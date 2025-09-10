from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from litestar import Litestar


def create_app() -> Litestar:
    """Create ASGI application using the core plugin pattern."""

    from litestar import Litestar

    from src.app.server.core import ApplicationCore
    from src.app.config.base import get_settings

    settings = get_settings()
    return Litestar(plugins=[ApplicationCore()], debug=settings.app.DEBUG)
