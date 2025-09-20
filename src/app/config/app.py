from __future__ import annotations

from typing import Literal, Tuple

import structlog

from litestar.logging.config import StructLoggingConfig
from litestar.plugins.structlog import StructlogConfig
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar_asyncpg import AsyncpgConfig, PoolConfig

from src.app.config.base import get_settings

settings = get_settings()

csrf = CSRFConfig(
    secret=settings.app.SECRET_KEY,
    cookie_name=settings.app.CSRF_COOKIE_NAME,
    cookie_secure=settings.app.CSRF_COOKIE_SECURE,
    safe_methods={
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    },
)

cors = CORSConfig(
    allow_origins=settings.app.ALLOWED_CORS_ORIGINS,
    allow_methods=[
        "GET",
        "POST",
        "DELETE",
        "PUT",
        "PATCH",
        "OPTIONS",
    ],
    allow_headers=["Origin", "Content-Type", "X-CSRFToken", "X-Access-Token"],
    allow_credentials=True,
)

compression = CompressionConfig(backend="gzip", gzip_compress_level=9)

rate_limit: Tuple[Literal["second"], int] = ("second", 10)
rate_limit_config = RateLimitConfig(rate_limit=rate_limit, exclude=["/schema"])

asyncpg = AsyncpgConfig(
    pool_config=PoolConfig(
        dsn=settings.db.DSN,
        min_size=settings.db.MIN_SIZE,
        max_size=settings.db.MAX_SIZE,
        max_queries=settings.db.MAX_QUERIES,
        max_inactive_connection_lifetime=settings.db.MAX_INACTIVE_CONNECTION_LIFETIME,
    )
)

log = StructlogConfig(
    structlog_logging_config=StructLoggingConfig(
        log_exceptions="always",
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
    ),
    middleware_logging_config=LoggingMiddlewareConfig(
        request_log_fields=["path", "method"],
        response_log_fields=["status_code"],
    ),
)
