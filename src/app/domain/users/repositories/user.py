from __future__ import annotations

from typing import Optional
from dataclasses import dataclass

from asyncpg import Connection

from src.app.domain.users.schemas import User


@dataclass
class UserRepository:
    """Repository for User operations using AsyncPG."""

    connection: Connection

    async def create(self, data: User) -> dict:
        """Create a new user."""
        query = """
            INSERT INTO users (name, email, password, role, status) 
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING id, name, email, role, status
        """
        return await self.connection.fetchrow(
            query, data.name, data.email, data.password, data.role, True
        )

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID."""
        query = "SELECT * FROM users WHERE id = $1"
        return await self.connection.fetchrow(query, user_id)

    async def get_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = $1"
        return await self.connection.fetchrow(query, email)

    async def email_exists(self, email: str) -> bool:
        """Check if email already exists."""
        query = "SELECT 1 FROM users WHERE email = $1"
        return bool(await self.connection.fetchrow(query, email))
