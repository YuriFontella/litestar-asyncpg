from __future__ import annotations

from litestar import MediaType, Router, get


@get(path="/", media_type=MediaType.JSON)
async def root() -> bool:
    return True


router = Router(path="/root", route_handlers=[root])
