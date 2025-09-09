from __future__ import annotations

from pathlib import Path

from litestar import Litestar

from .plugins import asyncpg_config


async def on_startup(app: Litestar) -> None:
    pool = asyncpg_config.provide_pool(app.state)
    async with pool.acquire() as conn:
        sql_path = (
            Path(__file__).resolve().parents[1] / "db" / "migrations" / "001_init.sql"
        )
        with sql_path.open("r", encoding="utf-8") as file:
            sql = file.read()
            await conn.execute(sql)


async def on_shutdown(app: Litestar) -> None:  # noqa: ARG001
    pass
