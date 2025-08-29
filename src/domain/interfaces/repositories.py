from abc import ABC, abstractmethod
from typing import Optional, List, Any

from src.domain.entities.common import User, Session, Team, Player


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, user: User) -> int:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass


class SessionRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, session: Session) -> int:
        pass

    @abstractmethod
    async def get_by_token_and_user_id(self, token: str, user_id: int) -> Optional[Session]:
        pass


class TeamRepositoryInterface(ABC):
    @abstractmethod
    async def create(self, team: Team) -> int:
        pass

    @abstractmethod
    async def get_all(self) -> List[Team]:
        pass


class PlayerRepositoryInterface(ABC):
    @abstractmethod
    async def create_many(self, players: List[Player]) -> bool:
        pass

    @abstractmethod
    async def get_by_team_id(self, team_id: int) -> List[Player]:
        pass