import asyncio
from litestar.events import listener
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend


class LitestarEventsAdapter:
    """Adapter for Litestar events and channels"""
    
    def __init__(self):
        self.channels_plugin = ChannelsPlugin(
            backend=MemoryChannelsBackend(),
            channels=['notifications'],
            create_ws_route_handlers=True
        )
    
    def get_channels_plugin(self) -> ChannelsPlugin:
        """Get the channels plugin"""
        return self.channels_plugin
    
    @staticmethod
    @listener('messages')
    async def on_message_listener(text: str) -> None:
        """Listener for messages event"""
        await asyncio.sleep(10)
        print(text)