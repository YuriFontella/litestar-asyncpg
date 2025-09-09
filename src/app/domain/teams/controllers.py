from __future__ import annotations

from litestar import Controller, Request, get, post
from litestar.di import Provide
from litestar.types import Scope
from litestar.status_codes import HTTP_201_CREATED
from litestar.exceptions import HTTPException

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
    """Team controller with CRUD operations."""

    path = "/teams"
    tags = ["Teams"]
    # Apply authentication middleware to all team routes
    middleware = [AuthenticationMiddleware]
    # Require team admin on all endpoints in this controller
    guards = [requires_team_admin]
    dependencies = {
        "teams_service": Provide(provide_teams_service, sync_to_thread=False)
    }

    @post(path=urls.TEAMS_PLAYERS, status_code=HTTP_201_CREATED)
    async def create_team_with_players(
        self,
        data: TeamWithPlayersCreate,
        scope: Scope,
        request: Request,
        teams_service: TeamsService,
    ) -> TeamRead:
        """Create a new team with players."""
        user = scope.get("user")

        # Check if team name already exists
        if await teams_service.team_name_exists(data.name):
            raise HTTPException(
                detail="Já existe um time com esse nome", status_code=400
            )

        try:
            team = await teams_service.create_with_players(
                data,
                owner_name=user["name"] if user else None,  # type: ignore[index]
            )

            request.app.emit("messages", "Seu time foi criado com sucesso!")
            return team

        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @get(path=urls.TEAMS_PLAYERS, cache=4)
    async def list_teams_with_players(
        self, teams_service: TeamsService
    ) -> list[TeamWithPlayersRead]:
        """List all teams with their players."""
        return await teams_service.list_with_players()

    @get(path="/{team_id:int}")
    async def get_team(self, team_id: int, teams_service: TeamsService) -> TeamRead:
        """Get team by ID."""
        team = await teams_service.get_team_by_id(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return team

    @get(path="/{team_id:int}/players")
    async def get_team_with_players(
        self, team_id: int, teams_service: TeamsService
    ) -> TeamWithPlayersRead:
        """Get team with players by ID."""
        team = await teams_service.get_team_with_players(team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return team
