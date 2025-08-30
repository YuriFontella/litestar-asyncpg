from litestar import Litestar
from config.plugin.asyncpg import config
from src.core.di.container import Container


async def on_startup(app: Litestar):
    # Initialize database tables
    pool = config.provide_pool(app.state)
    async with pool.acquire() as conn:
        with open('config/sql/tables.sql', 'r') as file:
            sql = file.read()
            await conn.execute(sql)

    # Initialize DI container and store in app state
    app.state.container = Container()


async def on_shutdown(app: Litestar):
    pass

