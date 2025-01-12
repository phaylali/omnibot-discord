import aiohttp
import asyncio
from datetime import datetime

class TrovoMonitor:
    def __init__(self, client_id):
        self.client_id = client_id
        self.monitored_channels = {}
        self.data_file = 'trovo_channels.json'
        self.load_channels()

    async def check_live_status(self, channel_name):
        async with aiohttp.ClientSession() as session:
            headers = {
                'Client-ID': self.client_id,
                'Accept': 'application/json'
            }
            url = f"https://open-api.trovo.live/openplatform/channels/username/{channel_name}"
            
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                is_live = data.get('is_live', False)
                return is_live, data if is_live else None
