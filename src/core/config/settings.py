from __future__ import annotations

from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv


load_dotenv()


def _get_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _get_list(name: str, default: List[str]) -> List[str]:
    val = os.getenv(name)
    if val is None or val.strip() == "":
        return default
    return [item.strip() for item in val.split(",") if item.strip()]


@dataclass(slots=True)
class Settings:
    # Security & DB
    key: str
    dsn: str
    access_token_salt: str
    jwt_alg: str

    # Asyncpg Pool
    asyncpg_min_size: int
    asyncpg_max_size: int

    # CSRF / CORS / Compression / Rate Limit
    csrf_secret: str
    cors_allow_origins: List[str]
    cors_allow_methods: List[str]
    cors_allow_headers: List[str]
    cors_allow_credentials: bool
    gzip_level: int
    rate_limit_unit: str
    rate_limit_rate: int
    rate_limit_exclude: List[str]

    # Channels
    channels: List[str]
    channels_create_ws: bool

    # Logging
    environment: str
    service_name: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        key = os.getenv("KEY", "")
        csrf_secret = os.getenv("CSRF_SECRET", key or "CHANGE_ME")
        return cls(
            key=key,
            dsn=os.getenv("DSN", ""),
            access_token_salt=os.getenv("ACCESS_TOKEN_SALT", "xYzDeV@0000"),
            jwt_alg=os.getenv("JWT_ALG", "HS256"),
            asyncpg_min_size=_get_int("ASYNC_PG_MIN_SIZE", 4),
            asyncpg_max_size=_get_int("ASYNC_PG_MAX_SIZE", 16),
            csrf_secret=csrf_secret,
            cors_allow_origins=_get_list("CORS_ALLOW_ORIGINS", ["*"]),
            cors_allow_methods=_get_list(
                "CORS_ALLOW_METHODS",
                ["GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"],
            ),
            cors_allow_headers=_get_list(
                "CORS_ALLOW_HEADERS",
                ["Origin", "Content-Type", "X-CSRFToken", "X-Access-Token"],
            ),
            cors_allow_credentials=_get_bool("CORS_ALLOW_CREDENTIALS", True),
            gzip_level=_get_int("GZIP_LEVEL", 9),
            rate_limit_unit=os.getenv("RATE_LIMIT_UNIT", "second"),
            rate_limit_rate=_get_int("RATE_LIMIT_RATE", 10),
            rate_limit_exclude=_get_list("RATE_LIMIT_EXCLUDE", ["/schema"]),
            channels=_get_list("CHANNELS", ["notifications"]),
            channels_create_ws=_get_bool("CHANNELS_CREATE_WS", True),
            environment=os.getenv("ENV", os.getenv("APP_ENV", "development")).lower(),
            service_name=os.getenv("SERVICE_NAME", "litestar-asyncpg-api"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


settings = Settings.from_env()
