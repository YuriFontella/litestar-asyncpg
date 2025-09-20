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
from src.app.config.base import get_settings


class ApplicationCore(InitPluginProtocol):
    """Plugin de configuração central da aplicação.

    Responsável por registrar handlers de rota, plugins, middlewares, listeners (eventos),
    dependências, ciclo de vida (startup/shutdown) e tratadores de exceção.
    """

    def on_app_init(self, app_config):
        from src.app.domain.users.controllers import UserController
        from src.app.domain.teams.controllers import TeamController
        from src.app.domain.root.controllers import RootController

        from src.app.domain.teams.signals import on_message

        # Registra os controllers (handlers de rota) e rota de arquivos estáticos
        # IMPORTANTE: a ordem aqui pode afetar resolução de conflitos de rota em alguns frameworks.
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

        # Registra plugins (ex: banco, canais, etc.)
        app_config.plugins.extend(get_plugins())

        # Configuração de segurança e CORS / compressão / CSRF
        app_config.cors_config = cors_config
        app_config.csrf_config = csrf_config
        app_config.compression_config = compression_config

        # Middleware globais (ordem importa: autenticação, rate limit, etc.)
        app_config.middleware.extend([factory, rate_limit_config.middleware])

        # Listeners / sinais (ex: canal de mensagens)
        app_config.listeners.extend([on_message])

        # Injeção de dependências disponíveis para handlers
        app_config.dependencies.update(
            {
                "current_user": Provide(provide_current_user, sync_to_thread=False),
            }
        )

        # Eventos de ciclo de vida da aplicação
        app_config.on_startup.extend([on_startup])
        app_config.on_shutdown.extend([on_shutdown])

        # Handlers de exceções customizados
        app_config.exception_handlers = {
            HTTPException: app_exception_handler,
            HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler,
        }

        # Modo debug: ativa PDB em exceções quando configurado
        settings = get_settings()
        app_config.pdb_on_exception = bool(settings.app.DEBUG)

        return app_config
