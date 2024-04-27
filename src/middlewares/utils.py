from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.compression import CompressionConfig
from litestar.middleware.rate_limit import RateLimitConfig

csrf_config = CSRFConfig(
    secret=str('SECRET_KEY'),
    safe_methods={
        'GET',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS'
    },
)

cors_config = CORSConfig(
    allow_origins=['*'],
    allow_methods=[
        'GET',
        'POST',
        'DELETE',
        'PUT',
        'PATCH',
        'OPTIONS',
    ],
    allow_headers=['Origin', 'Content-Type', 'X-CSRFToken', 'X-Access-Token'],
    allow_credentials=True
)

compression_config = CompressionConfig(backend='gzip', gzip_compress_level=9)

rate_limit_config = RateLimitConfig(rate_limit=('minute', 120), exclude=['/schema'])

