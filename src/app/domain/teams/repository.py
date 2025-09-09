from __future__ import annotations

import random
from typing import Optional
from dataclasses import dataclass

from asyncpg import Connection

from src.app.domain.teams.schemas import Team


@dataclass
class TeamRepository:
    """Repository for Team operations using AsyncPG."""

    connection: Connection

    async def create(self, data: Team) -> dict:
        """Create a new team with auto-generated protocol."""
        protocol = random.randint(111111, 999999)

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
        """Get team by ID."""
        query = "SELECT * FROM teams WHERE id = $1"
        return await self.connection.fetchrow(query, team_id)

    async def name_exists(self, name: str) -> bool:
        """Check if team name already exists."""
        query = "SELECT 1 FROM teams WHERE name = $1"
        return bool(await self.connection.fetchrow(query, name))


@dataclass
class PlayerRepository:
    """Repository for Player operations using AsyncPG."""

    connection: Connection

    async def create_many(self, players_data: list[tuple[str, int]]) -> bool:
        """Create multiple players for a team."""
        query = "INSERT INTO players (name, team_id) VALUES ($1, $2)"
        await self.connection.executemany(query, players_data)
        return True

    async def get_by_team(self, team_id: int) -> list[dict]:
        """Get all players for a team."""
        query = "SELECT * FROM players WHERE team_id = $1"
        return await self.connection.fetch(query, team_id)
