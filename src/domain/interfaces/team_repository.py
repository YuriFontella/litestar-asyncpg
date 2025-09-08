from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Any

from src.domain.entities.team import Team, Player


class TeamRepository(ABC):
    @abstractmethod
    async def upsert_team(self, conn: Any, team: Team) -> int:
        """Insert or update team and return id."""
        raise NotImplementedError

    @abstractmethod
    async def add_players(
        self, conn: Any, players: Iterable[Player], team_id: int
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def list_teams(self, conn: Any) -> List[Team]:
        raise NotImplementedError

    @abstractmethod
    async def list_players_by_team(self, conn: Any, team_id: int) -> List[Player]:
        raise NotImplementedError
