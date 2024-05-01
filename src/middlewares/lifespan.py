from litestar import Litestar
from config.plugin.asyncpg import config


async def on_startup(app: Litestar):
    pool = config.provide_pool(app.state)
    async with pool.acquire() as conn:
        with open('config/sql/tables.sql', 'r') as file:
            sql = file.read()
            await conn.execute(sql)


async def on_shutdown(app: Litestar):
    pass
