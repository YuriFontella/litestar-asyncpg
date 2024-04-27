from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig
from settings import dsn

asyncpg = AsyncpgPlugin(config=AsyncpgConfig(pool_config=PoolConfig(dsn=dsn)))
