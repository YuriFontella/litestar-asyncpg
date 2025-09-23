from __future__ import annotations

from typing import Dict

import msgspec
from litestar import Controller, get, post
from litestar.di import Provide
from litestar.types import Scope
from litestar.status_codes import HTTP_201_CREATED
from litestar.exceptions import HTTPException
from litestar.stores.registry import StoreRegistry

from src.app.lib.deps import EventEmitter
from src.app.domain.teams.guards import requires_team_admin
from src.app.domain.teams.schemas import (
    TeamWithPlayersCreate,
    TeamWithPlayersRead,
    TeamRead,
)
from src.app.server.auth import AuthenticationMiddleware
from src.app.domain.teams import urls
from src.app.domain.teams.deps import provide_teams_service
from src.app.domain.teams.services import TeamsService


class TeamController(Controller):
    """Controller de Times com operações de criação e consulta.

    Segurança:
    - Middleware de autenticação aplicado a todas as rotas.
    - Guard exige privilégio de administrador de time (ver `requires_team_admin`).
    """

    path = "/teams"
    tags = ["Teams"]
    # Aplica middleware de autenticação em todas as rotas de times
    middleware = [AuthenticationMiddleware]
    # Exige permissão de administrador (guard) em todos os endpoints
    guards = [requires_team_admin]
    dependencies = {
        "teams_service": Provide(provide_teams_service, sync_to_thread=False)
    }

    @post(path=urls.TEAMS_PLAYERS, status_code=HTTP_201_CREATED)
    async def create_team_with_players(
        self,
        data: TeamWithPlayersCreate,
        scope: Scope,
        teams_service: TeamsService,
        stores: StoreRegistry,
        emit: EventEmitter,
    ) -> TeamRead:
        """Cria novo time com jogadores em operação transacional."""
        user = scope.get("user")

        # Verifica se nome já está em uso
        if await teams_service.team_name_exists(data.name):
            raise HTTPException(
                detail="Já existe um time com esse nome", status_code=400
            )

        try:
            team = await teams_service.create_with_players(
                data,
                owner_name=user["name"] if user else None,
            )

            # Invalida cache após criar novo time
            store = stores.get("teams_cache")
            await store.delete("teams_list")

            emit("messages", "Seu time foi criado com sucesso!")
            return team

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @get(path=urls.TEAMS_PLAYERS)
    async def list_teams_with_players(
        self, teams_service: TeamsService, stores: StoreRegistry
    ) -> list[TeamWithPlayersRead]:
        """Lista todos os times com seus jogadores."""
        # Cache simples com store usando msgspec to_builtins/convert
        store = stores.get("teams_cache")
        cache_key = "teams_list"

        # Verifica se existe no cache
        cached_data = await store.get(cache_key)
        if cached_data:
            try:
                return msgspec.convert(cached_data, type=list[TeamWithPlayersRead])
            except (msgspec.ValidationError, msgspec.DecodeError):
                # Se falhar na conversão, remove do cache e continua
                await store.delete(cache_key)

        # Busca do banco e salva no cache
        teams = await teams_service.list_with_players()
        await store.set(cache_key, msgspec.to_builtins(teams), expires_in=60)

        return teams

    @get(path="/{team_id:int}", cache=4)
    async def get_team(self, team_id: int, teams_service: TeamsService) -> TeamRead:
        """Obtém time por ID."""
        team = await teams_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return team

    @get(path="/{team_id:int}/players", cache=4)
    async def get_team_with_players(
        self, team_id: int, teams_service: TeamsService, current_user: Dict
    ) -> TeamWithPlayersRead:
        """Obtém time e jogadores por ID."""
        print(current_user["email"] if current_user else "Anônimo")
        team = await teams_service.get_team_with_players(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return team
