from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig
from settings import dsn

config = AsyncpgConfig(pool_config=PoolConfig(dsn=dsn, min_size=4, max_size=12))
asyncpg = AsyncpgPlugin(config=config)
