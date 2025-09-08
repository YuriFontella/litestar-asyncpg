from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.compression import CompressionConfig
from litestar.middleware.rate_limit import RateLimitConfig

from src.core.config.settings import settings

csrf_config = CSRFConfig(
    secret=settings.csrf_secret,
    safe_methods={"GET", "POST", "DELETE", "PUT", "PATCH", "OPTIONS"},
)

cors_config = CORSConfig(
    allow_origins=settings.cors_allow_origins,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
    allow_credentials=settings.cors_allow_credentials,
)

compression_config = CompressionConfig(
    backend="gzip", gzip_compress_level=settings.gzip_level
)

rate_limit: tuple[str, int] = (settings.rate_limit_unit, settings.rate_limit_rate)
rate_limit_config = RateLimitConfig(
    rate_limit=rate_limit, exclude=settings.rate_limit_exclude
)
