from litestar import Litestar
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.static_files import create_static_files_router

from src.core.config import settings
from src.core.exceptions import app_exception_handler, internal_server_error_handler
from src.core.di import init_container, shutdown_container
from src.presentation import api_v1_router, AuthMiddleware
from src.infrastructure.adapters.litestar_asyncpg_adapter import LitestarAsyncpgAdapter
from src.infrastructure.adapters.litestar_config_adapter import LitestarConfigAdapter
from src.infrastructure.adapters.litestar_events_adapter import LitestarEventsAdapter

# Inicializa os adaptadores
db_adapter = LitestarAsyncpgAdapter()
config_adapter = LitestarConfigAdapter()
events_adapter = LitestarEventsAdapter()

# Obtém as configurações do Litestar
asyncpg_plugin = db_adapter.get_plugin()
channels_plugin = events_adapter.get_channels_plugin()
csrf_config = config_adapter.get_csrf_config()
cors_config = config_adapter.get_cors_config()
compression_config = config_adapter.get_compression_config()
rate_limit_config = config_adapter.get_rate_limit_config()


async def on_startup(app: Litestar) -> None:
    # Inicializa o container de injeção de dependência
    init_container()
    
    # Cria as tabelas no banco de dados
    pool = db_adapter.provide_pool(app.state)
    await db_adapter.execute_sql_file('config/sql/tables.sql')


async def on_shutdown(app: Litestar) -> None:
    # Libera os recursos do container
    shutdown_container()


app = Litestar(
    route_handlers=[
        api_v1_router,
        create_static_files_router(path='/public', directories=['public'], send_as_attachment=True)
    ],
    plugins=[asyncpg_plugin, channels_plugin],
    cors_config=cors_config,
    csrf_config=csrf_config,
    compression_config=compression_config,
    middleware=[AuthMiddleware, rate_limit_config.middleware],
    listeners=[events_adapter.on_message_listener],
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
    pdb_on_exception=False,
    exception_handlers={
        HTTPException: app_exception_handler,
        HTTP_500_INTERNAL_SERVER_ERROR: internal_server_error_handler
    },
    debug=settings.DEBUG
)
