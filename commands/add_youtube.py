import discord
from discord import app_commands
import logging

@app_commands.command(
    name="add-youtube",
    description="Add a YouTube channel to monitor"
)
async def add_youtube(
    interaction: discord.Interaction,
    channel_url: str
):
    # Check permissions
    streamer_role = discord.utils.get(interaction.guild.roles, name="Streamer")
    if streamer_role not in interaction.user.roles:
        await interaction.response.send_message(
            "You need the 'Streamer' role to use this command!",
            ephemeral=True
        )
        return

    # Check if in correct channel
    if interaction.channel.name != "streamer_submission":
        await interaction.response.send_message(
            "This command can only be used in the #streamer_submission channel!",
            ephemeral=True
        )
        return

    # Extract channel ID from URL
    try:
        channel_id = extract_channel_id(channel_url)
        is_valid = await interaction.client.youtube_monitor.check_live_status(channel_id)
        
        if is_valid:
            live_now_channel = discord.utils.get(interaction.guild.channels, name="live-now")
            await interaction.client.youtube_monitor.monitor_channel(
                channel_id,
                live_now_channel.id
            )
            
            await interaction.response.send_message(
                f"✅ Successfully added YouTube channel to monitoring!\nNotifications will be sent to {live_now_channel.mention}",
                ephemeral=True
            )
            logging.info(f"Added YouTube channel: {channel_id}")
        else:
            await interaction.response.send_message(
                "❌ Could not verify this YouTube channel. Please check the URL and try again.",
                ephemeral=True
            )
    except Exception as e:
        logging.error(f"Error adding YouTube channel: {str(e)}")
        await interaction.response.send_message(
            "❌ Error processing YouTube channel. Please check the URL format.",
            ephemeral=True
        )

def extract_channel_id(url: str) -> str:
    # Handle different YouTube URL formats
    if 'youtube.com/channel/' in url:
        return url.split('youtube.com/channel/')[1].split('/')[0]
    elif 'youtube.com/c/' in url:
        return url.split('youtube.com/c/')[1].split('/')[0]
    elif 'youtube.com/@' in url:
        return url.split('youtube.com/@')[1].split('/')[0]
    else:
        raise ValueError("Invalid YouTube URL format")

async def setup(bot):
    bot.tree.add_command(add_youtube)