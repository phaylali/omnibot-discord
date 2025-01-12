
import discord
from discord import app_commands
import logging

@app_commands.command(
    name="add-trovo",
    description="Add a Trovo channel to monitor"
)
async def add_trovo(
    interaction: discord.Interaction,
    channel_name: str
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

    try:
        is_live, channel_data = await interaction.client.trovo_monitor.check_live_status(channel_name)
        
        if channel_data:
            live_now_channel = discord.utils.get(interaction.guild.channels, name="live-now")
            await interaction.client.trovo_monitor.monitor_channel(
                channel_name,
                live_now_channel.id
            )
            
            await interaction.response.send_message(
                f"✅ Successfully added Trovo channel: {channel_name}\nNotifications will be sent to {live_now_channel.mention}",
                ephemeral=True
            )
            logging.info(f"Added Trovo channel: {channel_name}")
        else:
            await interaction.response.send_message(
                "❌ Could not verify this Trovo channel. Please check the channel name and try again.",
                ephemeral=True
            )
    except Exception as e:
        logging.error(f"Error adding Trovo channel: {str(e)}")
        await interaction.response.send_message(
            "❌ Error processing Trovo channel. Please check the channel name format.",
            ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(add_trovo)