import logging

from litestar import Litestar
from src.app.config import app as config
from src.app.config.constants import MIGRATIONS_DIR

logger = logging.getLogger(__name__)


async def on_startup(app: Litestar) -> None:
    pool = config.asyncpg.provide_pool(app.state)
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    async with pool.acquire() as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """
        )
        rows = await conn.fetch("SELECT filename FROM _migrations;")
        applied = set(row["filename"] for row in rows)
        for sql_path in migration_files:
            try:
                if sql_path.name in applied:
                    continue
                with sql_path.open("r", encoding="utf-8") as file:
                    sql = file.read()
                    async with conn.transaction():
                        await conn.execute(sql)
                        await conn.execute(
                            "INSERT INTO _migrations (filename) VALUES ($1);",
                            sql_path.name,
                        )
            except Exception as e:
                logger.exception("Error applying migration:", e)
                break


async def on_shutdown(app: Litestar) -> None:
    try:
        pool = config.asyncpg.provide_pool(app.state)
        if pool and not pool.is_closing():
            await pool.close()
    except Exception as e:
        logger.exception("Error closing database connection pool:", e)
