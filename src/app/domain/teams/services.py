from __future__ import annotations

from typing import Iterable
from dataclasses import dataclass, field

from asyncpg import Connection

from src.app.domain.teams.repository import TeamRepository, PlayerRepository
from src.app.domain.teams.schemas import (
    TeamWithPlayersCreate,
    TeamWithPlayersRead,
    PlayerRead,
    TeamRead,
)


@dataclass
class TeamsService:
    """Service layer for team/player operations using AsyncPG repositories."""

    connection: Connection
    team_repository: TeamRepository = field(init=False)
    player_repository: PlayerRepository = field(init=False)

    def __post_init__(self) -> None:
        self.team_repository = TeamRepository(self.connection)
        self.player_repository = PlayerRepository(self.connection)

    async def create_with_players(
        self, data: TeamWithPlayersCreate, owner_name: str | None = None
    ) -> TeamRead:
        """Create a team with players in a transaction."""
        async with self.connection.transaction():
            # Use provided owner or default
            team_owner = owner_name or data.owner

            # Create team data for repository
            from src.app.domain.teams.schemas import Team

            team_data = Team(
                name=data.name,
                price=data.price,
                owner=team_owner,
            )

            # Create team
            team_record = await self.team_repository.create(team_data)

            if not team_record:
                raise ValueError("Failed to create team")

            # Create players
            if data.players:
                players_data: Iterable[tuple[str, int]] = (
                    (player.name, team_record["id"]) for player in data.players
                )
                await self.player_repository.create_many(list(players_data))

        return TeamRead(
            id=team_record["id"],
            name=team_record["name"],
            price=team_record["price"],
            owner=team_record["owner"],
            protocol=team_record["protocol"],
            date=team_record["date"],
        )

    async def list_with_players(self) -> list[TeamWithPlayersRead]:
        """List all teams with their players."""
        teams = await self.connection.fetch("SELECT * FROM teams")
        response: list[TeamWithPlayersRead] = []

        for team_record in teams or []:
            # Get players for this team
            players_records = await self.player_repository.get_by_team(
                team_record["id"]
            )

            # Convert player records to PlayerRead schemas
            players = [
                PlayerRead(
                    id=player["id"],
                    name=player["name"],
                    language=player["language"],
                    uuid=player["uuid"],
                    status=player["status"],
                    team_id=player["team_id"],
                )
                for player in players_records
            ]

            # Create team with players
            team_with_players = TeamWithPlayersRead(
                id=team_record["id"],
                name=team_record["name"],
                price=team_record["price"],
                owner=team_record["owner"],
                protocol=team_record["protocol"],
                date=team_record["date"],
                players=players,
            )

            response.append(team_with_players)

        return response

    async def get_team_by_id(self, team_id: int) -> TeamRead | None:
        """Get team by ID."""
        team_record = await self.team_repository.get_by_id(team_id)
        if not team_record:
            return None

        return TeamRead(
            id=team_record["id"],
            name=team_record["name"],
            price=team_record["price"],
            owner=team_record["owner"],
            protocol=team_record["protocol"],
            date=team_record["date"],
        )

    async def get_team_with_players(self, team_id: int) -> TeamWithPlayersRead | None:
        """Get team with players by ID."""
        team_record = await self.team_repository.get_by_id(team_id)
        if not team_record:
            return None

        # Get players for this team
        players_records = await self.player_repository.get_by_team(team_id)

        players = [
            PlayerRead(
                id=player["id"],
                name=player["name"],
                language=player["language"],
                uuid=player["uuid"],
                status=player["status"],
                team_id=player["team_id"],
            )
            for player in players_records
        ]

        return TeamWithPlayersRead(
            id=team_record["id"],
            name=team_record["name"],
            price=team_record["price"],
            owner=team_record["owner"],
            protocol=team_record["protocol"],
            date=team_record["date"],
            players=players,
        )

    async def team_name_exists(self, name: str) -> bool:
        """Check if team name already exists."""
        return await self.team_repository.name_exists(name)
