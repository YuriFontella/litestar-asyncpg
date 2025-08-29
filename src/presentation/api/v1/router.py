from litestar import Router

from src.presentation.controllers import (
    RootController,
    UserController,
    TeamController,
    AuthController
)


api_v1_router = Router(
    path="/api/v1",
    route_handlers=[
        RootController,
        UserController,
        TeamController,
        AuthController
    ]
)