from __future__ import annotations

from litestar import Controller, MediaType, get
from src.app.domain.root import urls


class RootController(Controller):
    tags = ["Root"]

    @get(path=urls.ROOT, media_type=MediaType.JSON)
    async def index(self) -> bool:
        return True
