from __future__ import annotations

import secrets
from typing import Optional
from dataclasses import dataclass

from asyncpg import Connection

from src.app.domain.teams.schemas import Team


@dataclass
class TeamRepository:
    """Repositório para operações de Time usando AsyncPG.

    Nota: responsável apenas por acesso a dados (sem regra de negócio complexa).
    """

    connection: Connection

    async def create(self, data: Team) -> dict:
        """Cria novo time com protocolo gerado automaticamente."""
        protocol = secrets.randbelow(100_000_000)

        query = """
            INSERT INTO teams (name, price, protocol, owner)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (name)
            DO UPDATE SET price = EXCLUDED.price
            RETURNING id, name, price, protocol, owner, date
        """
        return await self.connection.fetchrow(
            query, data.name, data.price, protocol, data.owner
        )

    async def get_by_id(self, team_id: int) -> Optional[dict]:
        """Obtém time por ID."""
        query = "SELECT * FROM teams WHERE id = $1"
        return await self.connection.fetchrow(query, team_id)

    async def name_exists(self, name: str) -> bool:
        """Verifica se nome de time já existe."""
        query = "SELECT 1 FROM teams WHERE name = $1"
        return bool(await self.connection.fetchrow(query, name))


@dataclass
class PlayerRepository:
    """Repositório para operações de Jogador usando AsyncPG."""

    connection: Connection

    async def create_many(self, players_data: list[tuple[str, int]]) -> bool:
        """Cria múltiplos jogadores para um time (bulk insert)."""
        query = "INSERT INTO players (name, team_id) VALUES ($1, $2)"
        await self.connection.executemany(query, players_data)
        return True

    async def get_by_team(self, team_id: int) -> list[dict]:
        """Obtém todos os jogadores de um time."""
        query = "SELECT * FROM players WHERE team_id = $1"
        return await self.connection.fetch(query, team_id)
