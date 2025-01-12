import aiohttp
import asyncio
from datetime import datetime

class YouTubeMonitor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.monitored_channels = {}
        self.data_file = 'youtube_channels.json'
        self.load_channels()

    async def check_live_status(self, channel_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://www.googleapis.com/youtube/v3/search"
            params = {
                'key': self.api_key,
                'channelId': channel_id,
                'part': 'snippet',
                'type': 'video',
                'eventType': 'live'
            }
            
            async with session.get(url, params=params) as response:
                data = await response.json()
                return len(data['items']) > 0, data['items'][0] if data['items'] else None
