from __future__ import annotations

from litestar import Router, Controller, get, post
from litestar.types import Scope
from asyncpg import Connection

from typing import Any, Dict
from decimal import Decimal
from src.core.di.container import Container
from src.presentation.controllers.team_controller import TeamController
from src.domain.entities.team import Team, Player, TeamWithPlayers
from src.presentation.middlewares.auth import AuthenticationMiddleware

# Instantiate controller with DI container
container = Container()
team_controller = TeamController(
    create_uc=container.create_team_uc(),
    list_uc=container.list_teams_uc(),
)


class TeamsController(Controller):
    path = "/"

    @post(path="players")
    async def post_players(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        scope: Scope,
    ) -> bool:
        app = scope["app"]
        owner = scope.get("user")
        # Build domain entities from input
        team = Team(name=data["name"], price=Decimal(str(data["price"])), owner=owner)
        players = [Player(name=p["name"]) for p in data.get("players", [])]
        ok = await team_controller.create(db_connection, team, players, owner)
        if ok:
            app.emit("messages", "Seu time foi criado com sucesso!")
        return ok

    @get(path="players", cache=4)
    async def get_players(
        self,
        db_connection: Connection,
    ) -> list[TeamWithPlayers]:
        return await team_controller.list(db_connection)


router = Router(
    path="/teams",
    route_handlers=[TeamsController],
    middleware=[AuthenticationMiddleware],
)
