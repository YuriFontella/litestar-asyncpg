from __future__ import annotations

from litestar import Router, Controller, post, Request
from litestar.channels import ChannelsPlugin
from litestar.datastructures import State
from asyncpg import Connection

from typing import Any, Dict

from src.presentation.controllers.user_controller import (
    RegisterUserController,
    AuthenticateUserController,
)
from src.domain.entities.user import User, AuthCredentials
from src.domain.entities.token import Token


class UsersRoutes(Controller):
    path = "/"

    @post(path="register")
    async def register_user(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        channels: ChannelsPlugin,
        state: State,
    ) -> bool:
        user = User(**data)
        # Resolve controller from app container on demand
        container = state.container
        controller = RegisterUserController(use_case=container.register_user_uc())
        ok = await controller.register(db_connection, user)
        if ok:
            channels.publish("Usuário criado com sucesso!", channels=["notifications"])
        return ok

    @post(path="auth")
    async def auth_user(
        self,
        data: Dict[str, Any],
        db_connection: Connection,
        request: Request,
        state: State,
    ) -> Token:
        creds = AuthCredentials(**data)
        user_agent = request.headers.get("user-agent")
        ip = request.client.host if request.client else None
        container = state.container
        controller = AuthenticateUserController(
            use_case=container.authenticate_user_uc()
        )
        token = await controller.authenticate(db_connection, creds, user_agent, ip)
        return token


router = Router(path="/users", route_handlers=[UsersRoutes])
