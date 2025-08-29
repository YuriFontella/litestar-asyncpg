from typing import Optional, Any
from asyncpg import Connection, Pool
from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig

from settings import dsn


class DatabaseConnection:
    def __init__(self):
        self.config = AsyncpgConfig(pool_config=PoolConfig(dsn=dsn, min_size=4, max_size=16))
        self.plugin = AsyncpgPlugin(config=self.config)
        self._pool: Optional[Pool] = None

    async def get_connection(self, app_state: Any) -> Connection:
        if not self._pool:
            self._pool = self.config.provide_pool(app_state)
        return await self._pool.acquire()

    async def release_connection(self, connection: Connection) -> None:
        if self._pool:
            await self._pool.release(connection)


database = DatabaseConnection()
asyncpg_plugin = database.plugin