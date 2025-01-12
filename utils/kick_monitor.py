import aiohttp
import asyncio
from datetime import datetime

class KickMonitor:
    def __init__(self):
        self.monitored_channels = {}
        self.data_file = 'kick_channels.json'
        self.base_url = "https://kick.com/api/v1"
        self.load_channels()

    async def check_live_status(self, username):
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/channels/{username}"
            headers = {
                'Accept': 'application/json'
            }
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    is_live = data.get('livestream') is not None
                    return is_live, data if is_live else None
                return False, None
