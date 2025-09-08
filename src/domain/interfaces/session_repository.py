from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SessionRepository(ABC):
    @abstractmethod
    async def create_session(
        self,
        conn: Any,
        access_token: str,
        user_agent: str | None,
        ip: str | None,
        user_id: int,
    ) -> int:
        raise NotImplementedError
