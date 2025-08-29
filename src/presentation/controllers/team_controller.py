from typing import List
from litestar import Controller, get, post, Request
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_400_BAD_REQUEST

from src.core.di import container
from src.domain.entities.common import Team, Player
from src.presentation.schemas.team_schema import TeamSchema
from src.presentation.middlewares.auth_middleware import auth_required


class TeamController(Controller):
    path = "/teams"
    guards = [auth_required]

    @post("/players")
    async def create_team_with_players(self, data: TeamSchema, request: Request) -> bool:
        try:
            team_use_case = container.team_use_case()
            user = request.scope.get('user')
            
            # Criar entidade de time usando o método to_entity do schema
            team = data.to_entity()
            team.owner = user['name']
            
            # Garantir que os jogadores tenham team_id como None
            for player in team.players:
                player.team_id = None
            
            result = await team_use_case.create_team_with_players(team)
            if result:
                # Emitir evento de sucesso
                request.app.emit('messages', 'Seu time foi criado com sucesso!')
                
            return result
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=HTTP_400_BAD_REQUEST)

    @get("/players", cache=4)
    async def get_all_teams_with_players(self) -> List[TeamSchema]:
        try:
            team_use_case = container.team_use_case()
            teams = await team_use_case.get_all_teams_with_players()
            
            # Converter entidades para schemas usando o método de conversão
            return [TeamSchema.from_entity(team) for team in teams]
        except Exception as e:
            raise HTTPException(detail=str(e), status_code=HTTP_400_BAD_REQUEST)