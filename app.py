from litestar import Litestar
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from config.plugin.asyncpg import asyncpg
from config.exception.main import app_exception_handler, internal_server_error_handler

from src.middlewares.factory import factory
from src.middlewares.lifespan import on_startup, on_shutdown
from src.middlewares.utils import cors_config, csrf_config, compression_config, rate_limit_config

from src.controllers import players, users, root

app = Litestar(
    route_handlers=[
        players.router,
        users.router,
        root.router,
        create_static_files_router(path='/public', directories=['public'], send_as_attachment=True)
    ],
    plugins=[asyncpg],
    cors_config=cors_config,
    csrf_config=csrf_config,
    compression_config=compression_config,
    middleware=[factory, rate_limit_config.middleware],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    exception_handlers={
        HTTPException: app_exception_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler
    }
)
