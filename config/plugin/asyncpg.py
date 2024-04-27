from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig
from settings import dsn

config = AsyncpgConfig(pool_config=PoolConfig(dsn=dsn, min_size=2, max_size=8))
asyncpg = AsyncpgPlugin(config=config)
