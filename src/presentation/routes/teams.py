from __future__ import annotations

from litestar import Router, get, post, Request
from litestar.types import Scope
from asyncpg import Connection

from src.core.di.container import Container
from src.presentation.schemas.team_schemas import TeamCreateIn
from src.presentation.controllers.team_controller import TeamController
from src.domain.entities.team import Team, Player, TeamWithPlayers
from src.presentation.middlewares.auth import AuthenticationMiddleware


def build_team_controller(container: Container) -> TeamController:
    return TeamController(
        create_uc=container.create_team_uc(),
        list_uc=container.list_teams_uc(),
    )


@post(path="/players")
async def post_players(
    data: TeamCreateIn, db_connection: Connection, scope: Scope, request: Request
) -> bool:
    container: Container = request.app.state.container
    controller = build_team_controller(container)

    owner = scope.get("user", {}).get("name") if scope.get("user") else "unknown"
    team = Team(name=data.name, price=data.price)
    players = [Player(name=i.name) for i in data.players]

    ok = await controller.create(db_connection, team, players, owner)
    if ok:
        request.app.emit("messages", "Seu time foi criado com sucesso!")
    return ok


@get(path="/players", cache=4)
async def get_players(
    db_connection: Connection, request: Request
) -> list[TeamWithPlayers]:
    container: Container = request.app.state.container
    controller = build_team_controller(container)
    return await controller.list(db_connection)


router = Router(
    path="/teams",
    route_handlers=[post_players, get_players],
    middleware=[AuthenticationMiddleware],
)
