from __future__ import annotations

import logging
import sys
from functools import lru_cache
from typing import Literal, Tuple

import structlog
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.logging.config import (
    LoggingConfig,
    StructLoggingConfig,
    default_logger_factory,
    default_structlog_processors,
    default_structlog_standard_lib_processors,
)
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.plugins.structlog import StructlogConfig
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


@lru_cache
def _is_tty() -> bool:
    return bool(sys.stderr.isatty() or sys.stdout.isatty())


_render_as_json = not _is_tty()
_structlog_default_processors = default_structlog_processors(as_json=_render_as_json)
_structlog_default_processors.insert(1, structlog.processors.EventRenamer("message"))
_structlog_standard_lib_processors = default_structlog_standard_lib_processors(
    as_json=_render_as_json
)
_structlog_standard_lib_processors.insert(
    1, structlog.processors.EventRenamer("message")
)

log = StructlogConfig(
    structlog_logging_config=StructLoggingConfig(
        log_exceptions="always",
        processors=_structlog_default_processors,
        logger_factory=default_logger_factory(as_json=_render_as_json),
        standard_lib_logging_config=LoggingConfig(
            root={
                "level": logging.getLevelName(logging.INFO),
                "handlers": ["queue_listener"],
            },
            formatters={
                "standard": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": _structlog_standard_lib_processors,
                },
            },
        ),
    ),
    middleware_logging_config=LoggingMiddlewareConfig(
        request_log_fields=["path", "method", "query", "path_params"],
        response_log_fields=["status_code"],
    ),
)

asyncpg = AsyncpgConfig(
    pool_config=PoolConfig(
        dsn=settings.db.DSN,
        min_size=settings.db.MIN_SIZE,
        max_size=settings.db.MAX_SIZE,
        max_queries=settings.db.MAX_QUERIES,
        max_inactive_connection_lifetime=settings.db.MAX_INACTIVE_CONNECTION_LIFETIME,
    )
)
