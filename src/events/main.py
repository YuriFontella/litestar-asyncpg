import asyncio

from litestar.events import listener


@listener('send_email')
async def on_listener(email: str) -> None:
    await asyncio.sleep(10)
    print(email)
