
import discord
from discord import app_commands

@app_commands.command(
    name="list_channels",
    description="Lists all monitored channels"
)
async def list_channels(interaction: discord.Interaction):
    twitch_channels = list(interaction.client.stream_monitor.monitored_channels.get('twitch', {}).keys())
    youtube_channels = list(interaction.client.stream_monitor.monitored_channels.get('youtube', {}).keys())

    embed = discord.Embed(
        title="Monitored Channels",
        color=discord.Color.blue()
    )

    if twitch_channels:
        embed.add_field(name="Twitch Channels", value="\n".join(twitch_channels), inline=False)
    else:
        embed.add_field(name="Twitch Channels", value="No channels monitored", inline=False)

    if youtube_channels:
        embed.add_field(name="YouTube Channels", value="\n".join(youtube_channels), inline=False)
    else:
        embed.add_field(name="YouTube Channels", value="No channels monitored", inline=False)

    await interaction.response.send_message(embed=embed)

async def setup(bot):
    bot.tree.add_command(list_channels)
