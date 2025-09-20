from __future__ import annotations

import binascii
import os
from dataclasses import dataclass, field
from functools import lru_cache

from src.app.config.utils import get_env


@dataclass
class DatabaseSettings:
    """Database configuration for AsyncPG."""

    DSN: str = field(default_factory=lambda: get_env("DATABASE_DSN", ""))
    """AsyncPG Database connection string."""
    MIN_SIZE: int = field(default_factory=lambda: get_env("DATABASE_MIN_SIZE", 4))
    """Minimum pool size for AsyncPG connection pool."""
    MAX_SIZE: int = field(default_factory=lambda: get_env("DATABASE_MAX_SIZE", 16))
    """Maximum pool size for AsyncPG connection pool."""
    MAX_QUERIES: int = field(
        default_factory=lambda: get_env("DATABASE_MAX_QUERIES", 50000)
    )
    """Maximum number of queries per connection."""
    MAX_INACTIVE_CONNECTION_LIFETIME: float = field(
        default_factory=lambda: get_env(
            "DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME", 300.0
        )
    )
    """Maximum lifetime for inactive connections in seconds."""


@dataclass
class AppSettings:
    """Application configuration."""

    DEBUG: bool = field(default_factory=lambda: get_env("LITESTAR_DEBUG", False))
    """Run `Litestar` with `debug=True`."""
    SECRET_KEY: str = field(
        default_factory=lambda: get_env(
            "SECRET_KEY", binascii.hexlify(os.urandom(32)).decode(encoding="utf-8")
        ),
    )
    """Application secret key."""
    ALLOWED_CORS_ORIGINS: list[str] = field(
        default_factory=lambda: get_env("ALLOWED_CORS_ORIGINS", ["*"])
    )
    """Allowed CORS Origins."""
    CSRF_COOKIE_NAME: str = field(
        default_factory=lambda: get_env("CSRF_COOKIE_NAME", "XSRF-TOKEN")
    )
    """CSRF Cookie Name."""
    CSRF_COOKIE_SECURE: bool = field(
        default_factory=lambda: get_env("CSRF_COOKIE_SECURE", False)
    )
    """CSRF Secure Cookie."""
    JWT_ALGORITHM: str = field(
        default_factory=lambda: get_env("JWT_ALGORITHM", "HS256")
    )
    """JWT signing / encryption algorithm (e.g. HS256)."""
    SESSION_SALT: str = field(default_factory=lambda: get_env("SESSION_SALT", ""))
    """Static salt used for session token PBKDF2 derivation (change in production)."""
    DEFAULT_PLAYER_LANGUAGE: str = field(
        default_factory=lambda: get_env("DEFAULT_PLAYER_LANGUAGE", "pt-br")
    )
    """Default language assigned to players when not specified."""

    # Backwards compatibility: keep old attribute name if referenced elsewhere
    @property
    def JWT_ENCRYPTION_ALGORITHM(self) -> str:  # pragma: no cover - simple alias
        return self.JWT_ALGORITHM


@dataclass
class Settings:
    """Main application settings."""

    app: AppSettings = field(default_factory=AppSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)

    @classmethod
    def from_env(cls, dotenv_filename: str = ".env") -> Settings:
        """Load settings from environment file."""
        from pathlib import Path
        from dotenv import load_dotenv

        env_file = Path(f"{os.curdir}/{dotenv_filename}")
        if env_file.is_file():
            load_dotenv(env_file, override=True)
        return Settings()


@lru_cache(maxsize=1, typed=True)
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings.from_env()
