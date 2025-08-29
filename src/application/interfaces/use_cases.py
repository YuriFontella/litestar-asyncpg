from abc import ABC, abstractmethod
from typing import Optional, List

from src.domain.entities.common import User, Session, Team, Player


class UserUseCaseInterface(ABC):
    @abstractmethod
    async def register(self, user: User) -> bool:
        pass

    @abstractmethod
    async def authenticate(self, email: str, password: str, user_agent: str, ip: str) -> Optional[str]:
        pass

    @abstractmethod
    async def get_user_data(self, user_id: int) -> Optional[User]:
        pass


class TeamUseCaseInterface(ABC):
    @abstractmethod
    async def create_team_with_players(self, team: Team) -> bool:
        pass

    @abstractmethod
    async def get_all_teams_with_players(self) -> List[Team]:
        pass