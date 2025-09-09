from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers.base import BaseRouteHandler


def route_guards(connection: ASGIConnection, route: BaseRouteHandler) -> None:
    if connection.user["role"] != "admin":
        raise NotAuthorizedException()
