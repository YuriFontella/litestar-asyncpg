from __future__ import annotations

from pathlib import Path
from litestar import Litestar
from src.app.config import app as config

MIGRATIONS_DIR = Path(__file__).resolve().parent.parent / "db" / "migrations"


async def on_startup(app: Litestar) -> None:
    pool = config.asyncpg.provide_pool(app.state)
    migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    async with pool.acquire() as conn:
        # Ensure the migrations table exists
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS _migrations (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );
        """
        )
        # Get the set of already-applied migration filenames
        rows = await conn.fetch("SELECT filename FROM _migrations;")
        applied = set(row["filename"] for row in rows)
        for sql_path in migration_files:
            if sql_path.name in applied:
                continue
            with sql_path.open("r", encoding="utf-8") as file:
                sql = file.read()
                await conn.execute(sql)
                await conn.execute(
                    "INSERT INTO _migrations (filename) VALUES ($1);", sql_path.name
                )


async def on_shutdown(app: Litestar) -> None:
    pass
