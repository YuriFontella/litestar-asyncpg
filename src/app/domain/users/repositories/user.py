from __future__ import annotations

from typing import Optional
from dataclasses import dataclass

from asyncpg import Connection

from src.app.domain.users.schemas import User


@dataclass
class UserRepository:
    """Repositório para operações de Usuário usando AsyncPG."""

    connection: Connection

    async def create(self, data: User) -> dict:
        """Cria novo usuário."""
        query = """
            INSERT INTO users (name, email, password, role, status) 
            VALUES ($1, $2, $3, $4, $5) 
            RETURNING id, name, email, role, status
        """
        return await self.connection.fetchrow(
            query, data.name, data.email, data.password, data.role, True
        )

    async def get_by_id(self, user_id: int) -> Optional[dict]:
        """Obtém usuário por ID."""
        query = "SELECT * FROM users WHERE id = $1"
        return await self.connection.fetchrow(query, user_id)

    async def get_by_email(self, email: str) -> Optional[dict]:
        """Obtém usuário por e-mail."""
        query = "SELECT * FROM users WHERE email = $1"
        return await self.connection.fetchrow(query, email)

    async def email_exists(self, email: str) -> bool:
        """Verifica se e-mail já está cadastrado."""
        query = "SELECT 1 FROM users WHERE email = $1"
        return bool(await self.connection.fetchrow(query, email))
