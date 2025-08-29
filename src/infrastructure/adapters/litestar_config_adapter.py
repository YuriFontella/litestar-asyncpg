from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.config.compression import CompressionConfig
from litestar.middleware.rate_limit import RateLimitConfig

from src.core.config import settings


class LitestarConfigAdapter:
    """Adapter for Litestar configuration"""
    
    @staticmethod
    def get_csrf_config() -> CSRFConfig:
        """Get CSRF configuration"""
        return CSRFConfig(
            secret=settings.JWT_SECRET,
            safe_methods={
                'GET',
                'POST',
                'DELETE',
                'PUT',
                'PATCH',
                'OPTIONS'
            },
        )
    
    @staticmethod
    def get_cors_config() -> CORSConfig:
        """Get CORS configuration"""
        return CORSConfig(
            allow_origins=['*'],
            allow_methods=[
                'GET',
                'POST',
                'DELETE',
                'PUT',
                'PATCH',
                'OPTIONS',
            ],
            allow_headers=['Origin', 'Content-Type', 'X-CSRFToken', 'X-Access-Token', 'Authorization'],
            allow_credentials=True
        )
    
    @staticmethod
    def get_compression_config() -> CompressionConfig:
        """Get compression configuration"""
        return CompressionConfig(backend='gzip', gzip_compress_level=9)
    
    @staticmethod
    def get_rate_limit_config() -> RateLimitConfig:
        """Get rate limit configuration"""
        return RateLimitConfig(rate_limit=('second', 10), exclude=['/schema'])