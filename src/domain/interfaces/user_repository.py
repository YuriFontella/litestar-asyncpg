from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Any

from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, conn: Any, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, conn: Any, user: User) -> int:
        """Create a user and return id."""
        raise NotImplementedError

    @abstractmethod
    async def find_active_by_email(self, conn: Any, email: str) -> Optional[User]:
        raise NotImplementedError
