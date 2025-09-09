from __future__ import annotations

from litestar import Litestar
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from ..lib.exceptions import app_exception_handler, internal_server_error_handler
from .config import compression_config, cors_config, csrf_config, rate_limit_config
from .events import on_listener
from .lifespan import on_shutdown, on_startup
from .middleware import factory
from .plugins import get_plugins


def create_app() -> Litestar:
    from ..domain.accounts import routes as accounts
    from ..domain.teams import routes as teams
    from ..domain.web import routes as web

    return Litestar(
        route_handlers=[
            web.router,
            teams.router,
            accounts.router,
            create_static_files_router(
                path="/public", directories=["public"], send_as_attachment=True
            ),
        ],
        plugins=get_plugins(),
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
