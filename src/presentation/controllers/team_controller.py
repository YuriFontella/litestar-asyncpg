from __future__ import annotations

from dataclasses import dataclass
from typing import List
from asyncpg import Connection

from src.application.use_cases.create_team import CreateTeamUseCase
from src.application.use_cases.list_teams import ListTeamsUseCase
from src.domain.entities.team import Team, Player, TeamWithPlayers


@dataclass(slots=True)
class CreateTeamController:
    use_case: CreateTeamUseCase

    async def create(
        self, conn: Connection, team: Team, players: List[Player], owner: str
    ) -> bool:
        return await self.use_case.execute(conn, team, players, owner)


@dataclass(slots=True)
class ListTeamsController:
    use_case: ListTeamsUseCase

    async def list(self, conn: Connection) -> List[TeamWithPlayers]:
        return await self.use_case.execute(conn)
