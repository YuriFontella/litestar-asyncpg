from __future__ import annotations

from typing import Iterable
from dataclasses import dataclass
from functools import cached_property

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
    """Camada de serviço para operações de times/jogadores usando repositórios AsyncPG.

    Nota: mantém transações atômicas (ex: criação de time + jogadores) e
    converte registros do banco em schemas de leitura.
    """

    connection: Connection

    @cached_property
    def team_repository(self) -> TeamRepository:
        return TeamRepository(self.connection)

    @cached_property
    def player_repository(self) -> PlayerRepository:
        return PlayerRepository(self.connection)

    async def create_with_players(
        self, data: TeamWithPlayersCreate, owner_name: str | None = None
    ) -> TeamRead:
        """Cria um time com jogadores dentro de uma transação.

        Se qualquer parte falhar (ex: inserção de jogadores), toda a operação é revertida.
        """
        async with self.connection.transaction():
            # Usa owner explícito ou o informado no payload
            team_owner = owner_name or data.owner

            # Monta schema de criação
            from src.app.domain.teams.schemas import Team

            team_data = Team(
                name=data.name,
                price=data.price,
                owner=team_owner,
            )

            # Cria time
            team_record = await self.team_repository.create(team_data)

            if not team_record:
                raise ValueError("Failed to create team")

            # Cria jogadores (se enviados)
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
        """Lista todos os times com seus jogadores."""
        teams = await self.connection.fetch("SELECT * FROM teams")
        response: list[TeamWithPlayersRead] = []

        for team_record in teams or []:
            # Busca jogadores do time
            players_records = await self.player_repository.get_by_team(
                team_record["id"]
            )

            # Converte registros em schemas PlayerRead
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

            # Adiciona time com jogadores à resposta
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
        """Obtém time por ID."""
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
        """Obtém time e seus jogadores por ID."""
        team_record = await self.team_repository.get_by_id(team_id)
        if not team_record:
            return None

        # Busca jogadores deste time
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
        """Verifica se nome de time já existe."""
        return await self.team_repository.name_exists(name)
