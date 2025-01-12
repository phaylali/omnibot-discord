import discord
from discord import app_commands
from typing import Optional
import logging
import datetime

logging.basicConfig(
    filename='twitch_commands.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app_commands.command(
    name="add-twitch",
    description="Add a Twitch channel to monitor"
)
async def add_twitch(
    interaction: discord.Interaction,
    channel_name: str
):
    logging.info(f"Command executed by {interaction.user.name}#{interaction.user.discriminator} (ID: {interaction.user.id})")
    logging.info(f"Action: add, Channel: {channel_name}")

    # Role check
    streamer_role = discord.utils.get(interaction.guild.roles, name="Streamer")
    if streamer_role not in interaction.user.roles:
        logging.warning(f"Access denied: User lacks Streamer role")
        await interaction.response.send_message(
            "You need the 'Streamer' role to use this command!",
            ephemeral=True
        )
        return

    # Channel check
    if interaction.channel.name != "streamer_submission":
        logging.warning(f"Wrong channel: Command used in #{interaction.channel.name}")
        await interaction.response.send_message(
            "This command can only be used in the #streamer_submission channel!",
            ephemeral=True
        )
        return

    # Get live_now channel
    live_now_channel = discord.utils.get(interaction.guild.channels, name="live_now")
    if not live_now_channel:
        logging.error("live_now channel not found")
        await interaction.response.send_message(
            "The #live_now channel doesn't exist! Please create it first.",
            ephemeral=True
        )
        return

    # ADD command
    try:
        headers = {
            'Client-ID': interaction.client.twitch_monitor.client_id,
            'Authorization': f'Bearer {interaction.client.twitch_monitor.access_token}'
        }
        
        await interaction.client.twitch_monitor.monitor_channel(
            channel_name,
            live_now_channel.id
        )
        logging.info(f"Successfully added Twitch channel: {channel_name}")
        await interaction.response.send_message(
            f"✅ Now monitoring Twitch channel: {channel_name}\nLive notifications will be sent to {live_now_channel.mention}",
            ephemeral=True
        )
    except Exception as e:
        logging.error(f"Error adding channel {channel_name}: {str(e)}")
        await interaction.response.send_message(
            f"❌ Error adding the channel. Please try again later.",
            ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(add_twitch)