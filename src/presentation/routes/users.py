from __future__ import annotations

from litestar import Router, Request, post
from litestar.channels import ChannelsPlugin
from asyncpg import Connection

from src.core.di.container import Container
from src.presentation.schemas.user_schemas import UserRegisterIn, UserAuthIn
from src.presentation.controllers.user_controller import UserController
from src.domain.entities.user import User, AuthCredentials


def build_user_controller(container: Container) -> UserController:
    return UserController(
        register_uc=container.register_user_uc(),
        authenticate_uc=container.authenticate_user_uc(),
    )


@post(path='/register')
async def register_user(
    data: UserRegisterIn,
    db_connection: Connection,
    channels: ChannelsPlugin,
    request: Request,
) -> bool:
    container: Container = request.app.state.container
    controller = build_user_controller(container)
    user = User(name=data.name, email=data.email, password=data.password)
    ok = await controller.register(db_connection, user)
    if ok:
        channels.publish('Usuário criado com sucesso!', channels=['notifications'])
    return ok


@post(path='/auth')
async def auth_user(data: UserAuthIn, request: Request, db_connection: Connection):
    container: Container = request.app.state.container
    controller = build_user_controller(container)
    creds = AuthCredentials(email=data.email, password=data.password)
    user_agent = request.headers.get('user-agent')
    ip = request.client.host if request.client else None
    token = await controller.authenticate(db_connection, creds, user_agent, ip)
    return token


router = Router(path='/users', route_handlers=[register_user, auth_user])

