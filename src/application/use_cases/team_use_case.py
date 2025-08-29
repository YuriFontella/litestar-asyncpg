import random
from typing import List

from src.domain.entities.common import Team, Player
from src.domain.interfaces.repositories import TeamRepositoryInterface, PlayerRepositoryInterface
from src.application.interfaces.use_cases import TeamUseCaseInterface


class TeamUseCase(TeamUseCaseInterface):
    def __init__(self, team_repository: TeamRepositoryInterface, player_repository: PlayerRepositoryInterface):
        self.team_repository = team_repository
        self.player_repository = player_repository

    async def create_team_with_players(self, team: Team) -> bool:
        # Gerar protocolo aleatório se não fornecido
        if not team.protocol:
            team.protocol = random.randint(111111, 999999)

        # Criar time
        team_id = await self.team_repository.create(team)
        if not team_id:
            return False

        # Atualizar team_id nos jogadores
        for player in team.players:
            player.team_id = team_id

        # Criar jogadores
        if team.players:
            await self.player_repository.create_many(team.players)

        return True

    async def get_all_teams_with_players(self) -> List[Team]:
        teams = await self.team_repository.get_all()

        for team in teams:
            players = await self.player_repository.get_by_team_id(team.id)
            team.players = players

        return teams