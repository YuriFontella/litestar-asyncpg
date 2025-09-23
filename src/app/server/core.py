from __future__ import annotations

from litestar.di import Provide
from litestar.exceptions import HTTPException
from litestar.plugins import InitPluginProtocol
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router
from litestar.stores.registry import StoreRegistry

from src.app.lib.exceptions import app_exception_handler, internal_server_error_handler
from src.app.lib.deps import provide_current_user, provide_stores, provide_emit
from src.app.config.app import (
    compression as compression_config,
    cors as cors_config,
    csrf as csrf_config,
    allowed_hosts,
    rate_limit_config,
)
from src.app.server.lifespan import on_shutdown, on_startup
from src.app.server.middleware import factory
from src.app.server.stores import default_store
from src.app.server.plugins import get_plugins
from src.app.config.base import get_settings


class ApplicationCore(InitPluginProtocol):
    """Central application configuration plugin.

    Responsible for registering route handlers, plugins, middleware, listeners (events),
    dependencies, lifecycle (startup/shutdown) and exception handlers.
    """

    def on_app_init(self, app_config):
        from src.app.domain.users.controllers import UserController
        from src.app.domain.teams.controllers import TeamController
        from src.app.domain.root.controllers import RootController

        from src.app.domain.teams.signals import on_message

        # Register controllers (route handlers) and static files route
        # IMPORTANT: order here may affect route conflict resolution in some frameworks.
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

        # Register plugins (e.g.: database, channels, etc.)
        app_config.plugins.extend(get_plugins())

        # Security configuration and CORS / compression / CSRF / Allowed Hosts
        app_config.cors_config = cors_config
        app_config.csrf_config = csrf_config
        app_config.allowed_hosts = allowed_hosts
        app_config.compression_config = compression_config

        # Global middleware (order matters: authentication, rate limit, etc.)
        app_config.middleware.extend([factory, rate_limit_config.middleware])

        # Listeners / signals (e.g.: message channel)
        app_config.listeners.extend([on_message])

        # Dependency injection available for handlers
        app_config.dependencies.update(
            {
                "current_user": Provide(provide_current_user, sync_to_thread=False),
                "stores": Provide(provide_stores, sync_to_thread=False),
                "emit": Provide(provide_emit, sync_to_thread=False),
            }
        )

        # Store registry (e.g.: cache, session, etc.)
        app_config.stores = StoreRegistry(default_factory=default_store)

        # Application lifecycle events
        app_config.on_startup.extend([on_startup])
        app_config.on_shutdown.extend([on_shutdown])

        # Custom exception handlers
        app_config.exception_handlers = {
            HTTPException: app_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
        }

        # Debug mode: activates PDB on exceptions when configured
        settings = get_settings()
        app_config.pdb_on_exception = bool(settings.app.DEBUG)

        return app_config
