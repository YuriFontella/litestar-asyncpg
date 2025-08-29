import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class Settings:
    # Database
    DSN: str = os.getenv('DSN', '')
    
    # JWT
    JWT_SECRET: str = os.getenv('KEY', 'secret')
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # App
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    APP_NAME: str = 'Litestar AsyncPG API'
    APP_VERSION: str = '1.0.0'


settings = Settings()