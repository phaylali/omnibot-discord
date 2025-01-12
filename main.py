import os
import discord
import asyncio
from discord import app_commands
from dotenv import load_dotenv
from utils.config_manager import ConfigManager
from utils.platform_monitor import StreamMonitor, TwitchPlatform, TrovoPlatform, YoutubePlatform

# Load environment variables
load_dotenv()

# Initialize config manager
config_manager = ConfigManager()

# Bot class definition
class OmniversifyBot(discord.Client):
    def __init__(self):
        # Initialize with required intents
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        # Create command tree for slash commands
        self.tree = app_commands.CommandTree(self)
        
        # Initialize stream monitor
        self.stream_monitor = StreamMonitor()
        
        # Register platforms
        self.stream_monitor.register_platform(
            'twitch',
            TwitchPlatform(os.getenv('TWITCH_CLIENT_ID'), os.getenv('TWITCH_CLIENT_SECRET'))
        )
        

        self.stream_monitor.register_platform(
             'youtube',
            YoutubePlatform(os.getenv('YOUTUBE_API_KEY'))
        )

        # Add other platforms similarly        
    async def setup_hook(self):
        # Load all command files from the commands directory
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                # Import and setup each command
                module = __import__(f'commands.{filename[:-3]}', fromlist=['setup'])
                await module.setup(self)
                print(f"Loaded command: {filename[:-3]}")
        
        # Sync commands with Discord
        await self.tree.sync()
        print("Commands synced with Discord!")
        
        # Start stream monitoring (fixed reference)
        asyncio.create_task(self.stream_monitor.start_monitoring(self.handle_stream_online))

    async def handle_stream_online(self, discord_channel_id, streamer, title, game, thumbnail_url):
        channel = self.get_channel(discord_channel_id)
        if channel:
            # Get the Live role
            live_role = discord.utils.get(channel.guild.roles, name="Live")
            
            embed = discord.Embed(
                title=f"🔴 {streamer} is now live!",
                description=title,
                color=discord.Color.purple(),
                url=f"https://twitch.tv/{streamer}"
            )
            embed.add_field(name="Game", value=game)
            embed.set_thumbnail(url=thumbnail_url.replace("{width}x{height}", "128x128"))
            
            # Send notification with Live role mention
            message = await channel.send(
                content=f"{live_role.mention} **{streamer}** is streaming!",
                embed=embed
            )

            # If it's an announcement channel, publish the message
            if isinstance(channel, discord.TextChannel) and channel.is_news():
                await message.publish()# Initialize the bot
client = OmniversifyBot()

# Event: Bot is ready
@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    
    # Send online status to configured channels
    for channel_id in config_manager.get_status_channels():
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(f"🟢 Bot is now online! Ready to serve!")
    
    print('------')

# Run the bot with the token from .env
client.run(os.getenv('DISCORD_TOKEN'))
