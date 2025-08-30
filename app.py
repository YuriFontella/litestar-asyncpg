from litestar import Litestar
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from config.plugin.asyncpg import asyncpg
from config.exception.main import app_exception_handler, internal_server_error_handler

from src.presentation.channels.main import channels_plugin
from src.presentation.events.main import on_listener
from src.presentation.middlewares.factory import factory
from src.presentation.middlewares.lifespan import on_startup, on_shutdown
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
        create_static_files_router(path='/public', directories=['public'], send_as_attachment=True),
        auth.router,
    ],
    plugins=[asyncpg, channels_plugin],
    cors_config=cors_config,
    csrf_config=csrf_config,
    compression_config=compression_config,
    middleware=[factory, rate_limit_config.middleware],
    listeners=[on_listener],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    pdb_on_exception=False,
    exception_handlers={
        HTTPException: app_exception_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
    },
)
