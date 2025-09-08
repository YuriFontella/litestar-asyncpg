from __future__ import annotations

from typing import Optional
from asyncpg import Connection

from src.domain.entities.user import User as DomainUser
from src.domain.interfaces.user_repository import UserRepository
from src.infrastructure.database.queries.users import (
    FIND_BY_EMAIL,
    CREATE_USER,
    FIND_ACTIVE_BY_EMAIL,
)


class AsyncpgUserRepository(UserRepository):
    async def find_by_email(self, conn: Connection, email: str) -> Optional[DomainUser]:
        record = await conn.fetchrow(FIND_BY_EMAIL, email)
        if not record:
            return None
        return DomainUser(
            id=record["id"],
            name=record["name"],
            email=record["email"],
            password=record["password"],
            role=record["role"],
            status=record["status"],
        )

    async def create(self, conn: Connection, user: DomainUser) -> int:
        record = await conn.fetchrow(
            CREATE_USER,
            user.name,
            user.email,
            user.password,
            user.role,
            user.status,
        )
        return int(record["id"]) if record else 0

    async def find_active_by_email(
        self, conn: Connection, email: str
    ) -> Optional[DomainUser]:
        record = await conn.fetchrow(FIND_ACTIVE_BY_EMAIL, email)
        if not record:
            return None
        return DomainUser(
            id=record["id"],
            name=record["name"],
            email=record["email"],
            password=record["password"],
            role=record["role"],
            status=record["status"],
        )
