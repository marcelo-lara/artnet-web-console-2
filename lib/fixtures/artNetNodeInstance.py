from lib.fixtures.channel import Channel
import asyncio
from pyartnet import ArtNetNode

class ArtNetNodeInstance:
    _instance = None

    def __new__(cls, *args, **kwargs)->ArtNetNode:
        if not cls._instance:
            cls._instance = ArtNetNode(*args, **kwargs)
        return cls._instance
    
### helper
async def dispatch_artnet_packet(channel:Channel):

    # Get the ArtNet node and channel
    node = ArtNetNodeInstance()

    # Set next values and fade
    if channel.next_fade_duration is not None:
        channel.set_fade(channel.next_value, channel.next_fade_duration)
    else:
        channel.set_value(channel.next_value)

    # send and leave the node running
    node.start_refresh()
    await asyncio.sleep(0.01)