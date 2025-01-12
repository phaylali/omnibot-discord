
from abc import ABC, abstractmethod
import aiohttp
import asyncio
import json
import logging
from datetime import datetime
from utils.config_manager import ConfigManager

class StreamPlatform(ABC):
    @abstractmethod
    async def check_stream_status(self, channel_name):
        pass

    @abstractmethod
    async def get_stream_data(self, channel_name):
        pass

class TwitchPlatform(StreamPlatform):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expires_at = None

    async def get_access_token(self):
        async with aiohttp.ClientSession() as session:
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            async with session.post('https://id.twitch.tv/oauth2/token', data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.access_token = result['access_token']
                    self.token_expires_at = datetime.now().timestamp() + result['expires_in']
                    return self.access_token
                return None

    async def check_stream_status(self, channel_name):
        if not self.access_token or datetime.now().timestamp() >= self.token_expires_at:
            await self.get_access_token()

        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.twitch.tv/helix/streams?user_login={channel_name}', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return len(data['data']) > 0
                return False

    async def get_stream_data(self, channel_name):
        if not self.access_token or datetime.now().timestamp() >= self.token_expires_at:
            await self.get_access_token()

        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.twitch.tv/helix/streams?user_login={channel_name}', headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        return data['data'][0]
                return None

class TrovoPlatform(StreamPlatform):
    def __init__(self, client_id):
        self.client_id = client_id

    async def check_stream_status(self, channel_name):
        # Implement Trovo API calls
        pass

    async def get_stream_data(self, channel_name):
        # Implement Trovo stream data retrieval
        pass

class YoutubePlatform(StreamPlatform):
    def __init__(self, api_key):
        self.api_key = api_key

    async def check_stream_status(self, channel_name):
        # Implement YouTube API calls
        pass

    async def get_stream_data(self, channel_name):
        # Implement YouTube stream data retrieval
        pass

class StreamMonitor:
    def __init__(self):
        self.platforms = {}
        self.monitored_channels = {}
        self.config = ConfigManager()
        self._load_channels()

    def _load_channels(self):
        channel_data = self.config.get_monitored_channels()
        for platform, channels in channel_data.items():
            if platform not in self.monitored_channels:
                self.monitored_channels[platform] = {}
            for channel_name, discord_channel_id in channels.items():
                self.monitored_channels[platform][channel_name] = discord_channel_id

    def register_platform(self, platform_name, platform_instance):
        self.platforms[platform_name] = platform_instance

    async def start_monitoring(self, callback):
        while True:
            for platform_name, channels in self.monitored_channels.items():
                if platform_name in self.platforms:
                    platform = self.platforms[platform_name]
                    for channel_name, discord_channel_id in channels.items():
                        try:
                            is_live = await platform.check_stream_status(channel_name)
                            if is_live:
                                stream_data = await platform.get_stream_data(channel_name)
                                if stream_data:
                                    await callback(
                                        discord_channel_id,
                                        channel_name,
                                        stream_data['title'],
                                        stream_data['game_name'],
                                        stream_data['thumbnail_url']
                                    )
                        except Exception as e:
                            logging.error(f"Error monitoring {channel_name} on {platform_name}: {str(e)}")
            
            await asyncio.sleep(60)  # Check every minute
