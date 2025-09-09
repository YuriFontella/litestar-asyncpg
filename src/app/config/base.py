from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    key: str = os.getenv("KEY", "change-me")
    dsn: str = os.getenv("DSN", "")


settings = Settings()
