from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import random

from src.domain.entities.team import Team, Player
from src.domain.interfaces.team_repository import TeamRepository


@dataclass(slots=True)
class CreateTeamUseCase:
    team_repo: TeamRepository

    async def execute(
        self, conn: Any, team: Team, players: list[Player], owner: str
    ) -> bool:
        protocol = random.randint(111111, 999999)
        team.owner = owner
        team.protocol = protocol
        team_id = await self.team_repo.upsert_team(conn, team)
        if team_id:
            await self.team_repo.add_players(conn, players, team_id)
            return True
        return False
