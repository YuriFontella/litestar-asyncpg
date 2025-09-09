from __future__ import annotations

import asyncio

from litestar.events import listener


@listener("messages")
async def on_message(text: str) -> None:
    await asyncio.sleep(10)
    print(text)
