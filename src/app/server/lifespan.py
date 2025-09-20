from __future__ import annotations

from pathlib import Path
from litestar import Litestar
from src.app.server.plugins import asyncpg_config


async def on_startup(app: Litestar) -> None:
    pool = asyncpg_config.provide_pool(app.state)
    migrations_dir = Path(__file__).resolve().parent.parent / "db" / "migrations"
    migration_files = sorted(migrations_dir.glob("*.sql"))
    async with pool.acquire() as conn:
        for sql_path in migration_files:
            with sql_path.open("r", encoding="utf-8") as file:
                sql = file.read()
                await conn.execute(sql)


async def on_shutdown(app: Litestar) -> None:  # noqa: ARG001
    pass
