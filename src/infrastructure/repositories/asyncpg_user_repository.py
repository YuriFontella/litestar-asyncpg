from __future__ import annotations

from typing import Optional
from asyncpg import Connection

from src/domain.entities.user import User  # type: ignore
from src/domain/entities/user import User as DomainUser
from src/domain/interfaces/user_repository import UserRepository


class AsyncpgUserRepository(UserRepository):
    async def find_by_email(self, conn: Connection, email: str) -> Optional[DomainUser]:
        query = """
            select id, name, email, password, role, status
            from users
            where email = $1
            limit 1
        """
        record = await conn.fetchrow(query, email)
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
        query = """
            insert into users (name, email, password, role, status)
            values ($1, $2, $3, $4, coalesce($5, true))
            returning id
        """
        record = await conn.fetchrow(
            query,
            user.name,
            user.email,
            user.password,
            user.role,
            user.status,
        )
        return int(record["id"]) if record else 0

    async def find_active_by_email(self, conn: Connection, email: str) -> Optional[DomainUser]:
        query = """
            select id, name, email, password, role, status
            from users
            where email = $1 and status = true
            limit 1
        """
        record = await conn.fetchrow(query, email)
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

