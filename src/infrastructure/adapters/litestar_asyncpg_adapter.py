from typing import Optional, Any
from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig
from asyncpg import Pool

from src.core.config import settings


class LitestarAsyncpgAdapter:
    """Adapter for Litestar AsyncPG plugin"""
    
    def __init__(self):
        self.config = AsyncpgConfig(
            pool_config=PoolConfig(
                dsn=settings.DSN,
                min_size=4,
                max_size=16
            )
        )
        self.plugin = AsyncpgPlugin(config=self.config)
        self._pool: Optional[Pool] = None
    
    def get_plugin(self) -> AsyncpgPlugin:
        """Get the AsyncPG plugin for Litestar"""
        return self.plugin
    
    def get_config(self) -> AsyncpgConfig:
        """Get the AsyncPG configuration"""
        return self.config
    
    def provide_pool(self, state: Any) -> Pool:
        """Provide the connection pool from the state"""
        self._pool = self.config.provide_pool(state)
        return self._pool
    
    async def execute_sql_file(self, file_path: str) -> None:
        """Execute SQL from a file"""
        if not self._pool:
            raise ValueError("Pool not initialized. Call provide_pool first.")
            
        async with self._pool.acquire() as conn:
            with open(file_path, 'r') as file:
                sql = file.read()
                await conn.execute(sql)