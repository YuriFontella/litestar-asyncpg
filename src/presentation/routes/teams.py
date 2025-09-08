from __future__ import annotations

from litestar import Router, Controller, get, post
from litestar.datastructures import State
from litestar import Request
from asyncpg import Connection

from typing import Any, Dict
from decimal import Decimal
from src.presentation.controllers.team_controller import (
    CreateTeamController,
    ListTeamsController,
)
from src.domain.entities.team import Team, Player, TeamWithPlayers
from src.presentation.middlewares.auth import AuthenticationMiddleware


class TeamsRoutes(Controller):
    path = "/"

    @post(path="players")
    async def post_players(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        request: Request,
        state: State,
    ) -> bool:
        app = request.app
        user = request.user
        owner_name = user["name"] if isinstance(user, dict) else str(user)
        # Build domain entities from input
        team = Team(
            name=data["name"], price=Decimal(str(data["price"])), owner=owner_name
        )
        players = [Player(name=p["name"]) for p in data.get("players", [])]
        container = state.container
        controller = CreateTeamController(use_case=container.create_team_uc())
        ok = await controller.create(db_connection, team, players, owner_name)
        if ok:
            app.emit("messages", "Seu time foi criado com sucesso!")
        return ok

    @get(path="players", cache=4)
    async def get_players(
        self, db_connection: Connection, state: State
    ) -> list[TeamWithPlayers]:
        container = state.container
        controller = ListTeamsController(use_case=container.list_teams_uc())
        return await controller.list(db_connection)


router = Router(
    path="/teams",
    route_handlers=[TeamsRoutes],
    middleware=[AuthenticationMiddleware],
)
