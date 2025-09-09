from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.plugins.structlog import StructlogPlugin
from litestar_asyncpg import AsyncpgPlugin

from src.app.config import app as config

asyncpg_config = config.asyncpg
asyncpg = AsyncpgPlugin(config=asyncpg_config)
structlog = StructlogPlugin(config=config.log)


def get_plugins() -> list:
    channels = ChannelsPlugin(
        backend=MemoryChannelsBackend(),
        channels=["notifications"],
        create_ws_route_handlers=True,
    )
    return [structlog, asyncpg, channels]
