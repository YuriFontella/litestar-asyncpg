from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.exceptions import NotAuthorizedException


def route_guards(connection: ASGIConnection, route: BaseRouteHandler) -> None:
    if connection.user['role'] != 'admin':
        raise NotAuthorizedException()
