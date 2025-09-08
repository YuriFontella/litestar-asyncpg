import asyncio
from litestar.events import listener
from src.core.logging.config import get_logger


@listener("messages")
async def on_listener(text: str) -> None:
    await asyncio.sleep(10)
    logger = get_logger(__name__)
    logger.info("event_message", message=text)
