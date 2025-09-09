from __future__ import annotations

from typing import Annotated

from litestar.params import Dependency
from asyncpg import Connection

from src.app.domain.users.services import UsersService


def provide_users_service(
    db_connection: Annotated[Connection, Dependency(skip_validation=True)],
) -> UsersService:
    """Provide UsersService with database connection."""
    return UsersService(db_connection)
