import asyncio
from litestar.events import listener


@listener('messages')
async def on_listener(text: str) -> None:
    await asyncio.sleep(10)
    print(text)

