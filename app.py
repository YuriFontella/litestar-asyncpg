from litestar import Litestar
from litestar.events import EventListener
from typing import Sequence, cast
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from src.infrastructure.database.asyncpg import asyncpg
from src.core.exceptions.main import (
    app_exception_handler,
    internal_server_error_handler,
)

from src.presentation.channels.main import channels_plugin
from src.presentation.events.main import on_listener
from src.presentation.middlewares.factory import factory
from src.presentation.middlewares.utils import (
    cors_config,
    csrf_config,
    compression_config,
    rate_limit_config,
)

from src.presentation.routes import root, teams, users, auth

app = Litestar(
    route_handlers=[
        root.router,
        teams.router,
        users.router,
        create_static_files_router(
            path="/public", directories=["public"], send_as_attachment=True
        ),
        auth.router,
    ],
    plugins=[asyncpg, channels_plugin],
    cors_config=cors_config,
    csrf_config=csrf_config,
    compression_config=compression_config,
    middleware=[factory, rate_limit_config.middleware],
    listeners=cast(Sequence[EventListener], [on_listener]),
    pdb_on_exception=False,
    exception_handlers={
        HTTPException: app_exception_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
)
