from __future__ import annotations

from asyncpg import Connection

from src.domain.interfaces.session_repository import SessionRepository
from src.infrastructure.database.queries.sessions import CREATE_SESSION


class AsyncpgSessionRepository(SessionRepository):
    async def create_session(
        self,
        conn: Connection,
        access_token: str,
        user_agent: str | None,
        ip: str | None,
        user_id: int,
    ) -> int:
        record = await conn.fetchrow(
            CREATE_SESSION, access_token, user_agent, ip, user_id
        )
        return int(record["id"]) if record else 0
