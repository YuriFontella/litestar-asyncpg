from __future__ import annotations

from asyncpg import Connection

from src/domain/interfaces/session_repository import SessionRepository


class AsyncpgSessionRepository(SessionRepository):
    async def create_session(
        self,
        conn: Connection,
        access_token: str,
        user_agent: str | None,
        ip: str | None,
        user_id: int,
    ) -> int:
        query = """
            insert into sessions (access_token, user_agent, ip, user_id) 
            values ($1, $2, $3, $4) returning id
        """
        record = await conn.fetchrow(query, access_token, user_agent, ip, user_id)
        return int(record["id"]) if record else 0

