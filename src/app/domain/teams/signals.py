from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from litestar.events import listener

if TYPE_CHECKING:
    from litestar.events import EventListener


@listener("messages")
async def on_message(text: str) -> None:
    await asyncio.sleep(10)
    print(text)


# Type annotation for the listener
on_message: EventListener
