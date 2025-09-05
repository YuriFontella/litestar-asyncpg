from __future__ import annotations

from litestar import Router, Controller, post, Request
from litestar.channels import ChannelsPlugin
from asyncpg import Connection

from typing import Any, Dict
from src.core.di.container import Container
from src.presentation.controllers.user_controller import UserController
from src.domain.entities.user import User, AuthCredentials
from src.domain.entities.token import Token

# Instanciação de controller via DI
container = Container()
user_controller = UserController(
    register_uc=container.register_user_uc(),
    authenticate_uc=container.authenticate_user_uc(),
)


class UsersController(Controller):
    path = "/"

    @post(path="register")
    async def register_user(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        channels: ChannelsPlugin,
    ) -> bool:
        user = User(**data)
        ok = await user_controller.register(db_connection, user)
        if ok:
            channels.publish("Usuário criado com sucesso!", channels=["notifications"])
        return ok

    @post(path="auth")
    async def auth_user(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        request: Request,
    ) -> Token:
        creds = AuthCredentials(**data)
        user_agent = request.headers.get("user-agent")
        ip = request.client.host if request.client else None
        token = await user_controller.authenticate(db_connection, creds, user_agent, ip)
        return token


router = Router(path="/users", route_handlers=[UsersController])
