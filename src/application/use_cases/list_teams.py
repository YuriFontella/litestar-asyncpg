from __future__ import annotations

from dataclasses import dataclass
from typing import List, Any

from src.domain.entities.team import TeamWithPlayers
from src.domain.interfaces.team_repository import TeamRepository


@dataclass(slots=True)
class ListTeamsUseCase:
    team_repo: TeamRepository

    async def execute(self, conn: Any) -> List[TeamWithPlayers]:
        teams = await self.team_repo.list_teams(conn)
        result: list[TeamWithPlayers] = []
        for t in teams:
            players = await self.team_repo.list_players_by_team(conn, int(t.id or 0))
            result.append(
                TeamWithPlayers(
                    id=t.id,
                    name=t.name,
                    price=t.price,
                    owner=t.owner,
                    protocol=t.protocol,
                    date=t.date,
                    players=players,
                )
            )
        return result
