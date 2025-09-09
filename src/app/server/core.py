from __future__ import annotations

from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.plugins import InitPluginProtocol
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from src.app.lib.exceptions import app_exception_handler, internal_server_error_handler
from src.app.lib.deps import provide_current_user
from src.app.config.app import (
    compression as compression_config,
    cors as cors_config,
    csrf as csrf_config,
    rate_limit_config,
)
from src.app.server.lifespan import on_shutdown, on_startup
from src.app.server.middleware import factory
from src.app.server.plugins import get_plugins


class ApplicationCore(InitPluginProtocol):
    """Core application configuration plugin."""

    def on_app_init(self, app_config):  # type: ignore[override]
        from src.app.domain.users.controllers import UserController
        from src.app.domain.teams.controllers import TeamController
        from src.app.domain.root.controllers import RootController

        from src.app.domain.teams.signals import on_message

        # Register route handlers
        app_config.route_handlers.extend(
            [
                RootController,
                TeamController,
                UserController,
                create_static_files_router(
                    path="/public", directories=["public"], send_as_attachment=True
                ),
            ]
        )

        # Register plugins
        app_config.plugins.extend(get_plugins())

        # Security and CORS configuration
        app_config.cors_config = cors_config
        app_config.csrf_config = csrf_config
        app_config.compression_config = compression_config

        # Middleware
        app_config.middleware.extend([factory, rate_limit_config.middleware])

        # Event listeners
        app_config.listeners.extend([on_message])

        # Dependency injection
        app_config.dependencies.update(
            {
                "current_user": Provide(provide_current_user, sync_to_thread=False),
            }
        )

        # Application lifecycle
        app_config.on_startup.extend([on_startup])
        app_config.on_shutdown.extend([on_shutdown])

        # Exception handlers
        app_config.exception_handlers = {
            HTTPException: app_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
        }

        # Debug configuration
        app_config.pdb_on_exception = False

        return app_config
