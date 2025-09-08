from litestar import Litestar
from src.infrastructure.database.asyncpg import config


async def on_startup(app: Litestar):
    # Initialize database tables
    pool = config.provide_pool(app.state)
    async with pool.acquire() as conn:
        with open("src/infrastructure/database/sql/tables.sql", "r") as file:
            sql = file.read()
        await conn.execute(sql)


async def on_shutdown(app: Litestar):
    pass
