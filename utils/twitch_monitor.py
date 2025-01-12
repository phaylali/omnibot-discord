import aiohttp
import asyncio
import json
import os
import logging
from datetime import datetime, timedelta

class TwitchMonitor:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.monitored_channels = {}
        self.callback = None
        self.data_file = 'monitored_channels.json'
        
        # Set up logging
        logging.basicConfig(
            filename='twitch_monitor.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )
        self.load_channels()

    def load_channels(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.monitored_channels = {
                    channel: {
                        'discord_channel': info['discord_channel'],
                        'last_status': False,  # Reset status on load
                        'last_notification': None,
                        'cooldown_until': None
                    }
                    for channel, info in data.items()
                }
                logging.info(f"Loaded channels: {list(self.monitored_channels.keys())}")

    def save_channels(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.monitored_channels, f, indent=4)
        logging.info("Saved channel data")

    async def get_access_token(self):
        async with aiohttp.ClientSession() as session:
            params = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            async with session.post('https://id.twitch.tv/oauth2/token', params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    self.access_token = data['access_token']
                    return True
                return False

    async def check_stream_status(self, username):
        if not self.access_token:
            await self.get_access_token()

        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'https://api.twitch.tv/helix/streams?user_login={username}',
                headers=headers
            ) as response:
                if response.status == 200:
                    stream_data = await response.json()
                    if stream_data['data']:
                        return True, {
                            'title': stream_data['data'][0].get('title', 'Live Stream'),
                            'game_name': stream_data['data'][0].get('game_name', 'Gaming'),
                            'thumbnail_url': stream_data['data'][0].get('thumbnail_url', '')
                        }
                    return False, None
                return False, None

    async def monitor_channel(self, channel_name, discord_channel_id):
        self.monitored_channels[channel_name] = {
            'discord_channel': discord_channel_id,
            'last_status': False,
            'last_notification': None,
            'cooldown_until': None
        }
        self.save_channels()
        logging.info(f"Added channel to monitor: {channel_name}")

    async def remove_channel(self, channel_name):
        if channel_name in self.monitored_channels:
            del self.monitored_channels[channel_name]
            self.save_channels()  # Save after removing
            return True
        return False

    async def start_monitoring(self, callback):
        self.callback = callback
        logging.info("Starting monitor loop")
        while True:
            current_time = datetime.now()
            
            for channel_name in list(self.monitored_channels.keys()):
                try:
                    channel_data = self.monitored_channels[channel_name]
                    
                    # Check cooldown
                    if channel_data.get('cooldown_until'):
                        cooldown_time = datetime.fromisoformat(channel_data['cooldown_until'])
                        if current_time < cooldown_time:
                            continue
                        channel_data['cooldown_until'] = None
                    
                    is_live, stream_data = await self.check_stream_status(channel_name)
                    logging.info(f"Channel {channel_name} status check - Live: {is_live}")
                    
                    if is_live and not channel_data['last_status']:
                        discord_channel = channel_data['discord_channel']
                        
                        # Check if enough time has passed since last notification
                        last_notif = channel_data.get('last_notification')
                        if last_notif:
                            last_notif_time = datetime.fromisoformat(last_notif)
                            if (current_time - last_notif_time) < timedelta(minutes=2):
                                continue
                        
                        if stream_data:
                            await self.callback(
                                discord_channel,
                                channel_name,
                                stream_data['title'],
                                stream_data['game_name'],
                                stream_data['thumbnail_url']
                            )
                            logging.info(f"Sent notification for {channel_name}")
                            
                            # Update notification time and status
                            channel_data['last_notification'] = current_time.isoformat()
                            channel_data['last_status'] = True
                            self.save_channels()
                    
                    elif not is_live and channel_data['last_status']:
                        # Set cooldown when stream goes offline
                        channel_data['last_status'] = False
                        channel_data['cooldown_until'] = (current_time + timedelta(minutes=2)).isoformat()
                        self.save_channels()
                        logging.info(f"Stream went offline: {channel_name}, cooldown set")
                
                except Exception as e:
                    logging.error(f"Error monitoring {channel_name}: {str(e)}")
            
            await asyncio.sleep(60)