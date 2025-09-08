from __future__ import annotations

from typing import Iterable, List
from asyncpg import Connection

from src.domain.entities.team import Team, Player
from src.domain.interfaces.team_repository import TeamRepository
from src.infrastructure.database.queries.teams import (
    UPSERT_TEAM,
    LIST_TEAMS,
    LIST_PLAYERS_BY_TEAM,
)


class AsyncpgTeamRepository(TeamRepository):
    async def upsert_team(self, conn: Connection, team: Team) -> int:
        record = await conn.fetchrow(
            UPSERT_TEAM, team.name, team.price, team.protocol, team.owner
        )
        return int(record["id"]) if record else 0

    async def add_players(
        self, conn: Connection, players: Iterable[Player], team_id: int
    ) -> None:
        data = [(p.name, team_id) for p in players]
        if data:
            await conn.executemany(
                "insert into players (name, team_id) values ($1, $2)", data
            )

    async def list_teams(self, conn: Connection) -> List[Team]:
        records = await conn.fetch(LIST_TEAMS)
        return [
            Team(
                id=r["id"],
                name=r["name"],
                price=r["price"],
                owner=r["owner"],
                protocol=r["protocol"],
                date=r["date"],
            )
            for r in records
        ]

    async def list_players_by_team(self, conn: Connection, team_id: int):
        records = await conn.fetch(LIST_PLAYERS_BY_TEAM, team_id)
        return [
            Player(
                id=r["id"],
                name=r["name"],
                language=r["language"],
                uuid=str(r["uuid"]) if r["uuid"] else None,
                status=r["status"],
                team_id=r["team_id"],
            )
            for r in records
        ]
