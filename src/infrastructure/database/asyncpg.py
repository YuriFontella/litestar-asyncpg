from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig
from src.core.config.settings import settings

config = AsyncpgConfig(
    pool_config=PoolConfig(
        dsn=settings.dsn,
        min_size=settings.asyncpg_min_size,
        max_size=settings.asyncpg_max_size,
    )
)
asyncpg = AsyncpgPlugin(config=config)
