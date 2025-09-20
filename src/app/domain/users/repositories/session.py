from __future__ import annotations

from typing import Optional
from dataclasses import dataclass

from asyncpg import Connection


@dataclass
class SessionRepository:
    """Repository for Session operations using AsyncPG."""

    connection: Connection

    async def create(
        self, access_token: str, user_agent: str | None, ip: str | None, user_id: int
    ) -> dict:
        """Create a new session."""
        query = """
            INSERT INTO sessions (access_token, user_agent, ip, user_id) 
            VALUES ($1, $2, $3, $4) 
            RETURNING id, access_token, user_id, date
        """
        return await self.connection.fetchrow(
            query, access_token, user_agent, ip, user_id
        )

    async def get_by_token(self, access_token: str) -> Optional[dict]:
        """Get session by access token."""
        query = "SELECT * FROM sessions WHERE access_token = $1 AND revoked = false"
        return await self.connection.fetchrow(query, access_token)

    async def revoke(self, session_id: int) -> bool:
        """Revoke session by ID."""
        query = "UPDATE sessions SET revoked = true WHERE id = $1"
        result = await self.connection.execute(query, session_id)
        return result == "UPDATE 1"

    async def revoke_by_user(self, user_id: int) -> bool:
        """Revoke all sessions for a user."""
        query = "UPDATE sessions SET revoked = true WHERE user_id = $1"
        result = await self.connection.execute(query, user_id)
        return len(result) > 0
