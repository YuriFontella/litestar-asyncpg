from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig

from ..config import settings

asyncpg_config = AsyncpgConfig(
    pool_config=PoolConfig(dsn=settings.dsn, min_size=4, max_size=16)
)
asyncpg = AsyncpgPlugin(config=asyncpg_config)


def get_plugins() -> list:
    channels = ChannelsPlugin(
        backend=MemoryChannelsBackend(),
        channels=["notifications"],
        create_ws_route_handlers=True,
    )
    return [asyncpg, channels]
