from .fixture import Channel
from .parCan import ParCan
from .head import Head
from .channel import Channel
from .artNetNodeInstance import ArtNetNodeInstance
import yaml
import os

# Define Art-Net defaults
ARTNET_NODE_IP = os.getenv('ARTNET_NODE_IP', '192.168.1.221')
FADE_TIME = int(os.getenv('ARTNET_DEFAULT_FADETIME', '1'))

fixture_types = {
    'Head': Head,
    'ParCan': ParCan
}

fixtures = []

def load_fixtures(path: str = 'fixtures.yaml'):
    global fixtures
    with open(path, 'r') as file:
        fixtures_data = yaml.safe_load(file)
    fixtures = [create_fixture(data) for data in fixtures_data]    
    return fixtures

def create_fixture(data):
    fixture_type = data.get('type')
    if fixture_type in fixture_types:
        return fixture_types[fixture_type](**data)
    else:
        raise ValueError(f"Unknown fixture type: {fixture_type}")
    
async def async_setup_artnet(fixture_config_path=None, artnet_channels=[]):
    print("Setting up ArtNet fixtures")
    global fixtures

    if fixture_config_path:
        fixtures = load_fixtures(fixture_config_path)

    if not fixtures:
        fixtures = load_fixtures()

    node = ArtNetNodeInstance(ARTNET_NODE_IP, 6454)
    universe = node.add_universe(0)
    for fixture in fixtures:
        for channel in fixture.channels:
            channel._instance = universe.add_channel(start=channel.number, width=channel.channel_width, channel_name=channel.id)
            _channel = {
                'name': channel.id,
                'instance': channel
            }
            artnet_channels.append(_channel)
    universe._resize_universe(512)
    
    print(f"{len(fixtures)} fixtures")