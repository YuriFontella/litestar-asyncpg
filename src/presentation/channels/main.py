from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend

from src.core.config.settings import settings

channels_plugin = ChannelsPlugin(
    backend=MemoryChannelsBackend(),
    channels=settings.channels,
    create_ws_route_handlers=settings.channels_create_ws,
)
