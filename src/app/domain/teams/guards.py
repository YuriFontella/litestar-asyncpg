from __future__ import annotations

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def requires_team_admin(connection: ASGIConnection, route: BaseRouteHandler) -> None:
    """Simple guard ensuring the authenticated user has admin role for team endpoints."""
    user = getattr(connection, "user", None)
    if not user or user.get("role") != "admin":
        raise NotAuthorizedException()
