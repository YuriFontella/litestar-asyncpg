from __future__ import annotations

from typing import Annotated

from litestar.params import Dependency
from asyncpg import Connection

from src.app.domain.teams.services import TeamsService


def provide_teams_service(
    db_connection: Annotated[Connection, Dependency(skip_validation=True)],
) -> TeamsService:
    """Provide TeamsService with database connection."""
    return TeamsService(db_connection)
