from __future__ import annotations

from dataclasses import dataclass
from typing import List
from asyncpg import Connection

from src.application.use_cases.create_team import CreateTeamUseCase
from src.application.use_cases.list_teams import ListTeamsUseCase
from src.domain.entities.team import Team, Player, TeamWithPlayers


@dataclass(slots=True)
class TeamController:
    create_uc: CreateTeamUseCase
    list_uc: ListTeamsUseCase

    async def create(self, conn: Connection, team: Team, players: List[Player], owner: str) -> bool:
        return await self.create_uc.execute(conn, team, players, owner)

    async def list(self, conn: Connection) -> List[TeamWithPlayers]:
        return await self.list_uc.execute(conn)

