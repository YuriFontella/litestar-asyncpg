from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List
from asyncpg import Connection

from src/domain/entities/team import Team, Player, TeamWithPlayers


class TeamRepository(ABC):
    @abstractmethod
    async def upsert_team(self, conn: Connection, team: Team) -> int:
        """Insert or update team and return id."""
        raise NotImplementedError

    @abstractmethod
    async def add_players(self, conn: Connection, players: Iterable[Player], team_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_teams(self, conn: Connection) -> List[Team]:
        raise NotImplementedError

    @abstractmethod
    async def list_players_by_team(self, conn: Connection, team_id: int) -> List[Player]:
        raise NotImplementedError

