
import discord
from discord import app_commands
import logging

@app_commands.command(
    name="add-tiktok",
    description="Add a TikTok channel to monitor"
)
async def add_tiktok(
    interaction: discord.Interaction,
    username: str
):
    # Clean up username input (remove @ if present)
    username = username.strip('@')

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
        is_valid, channel_data = await interaction.client.tiktok_monitor.check_live_status(username)
        
        if is_valid:
            live_now_channel = discord.utils.get(interaction.guild.channels, name="live-now")
            await interaction.client.tiktok_monitor.monitor_channel(
                username,
                live_now_channel.id
            )
            
            embed = discord.Embed(
                title="TikTok Channel Added",
                description=f"Successfully added @{username} to monitoring",
                color=discord.Color.brand_red()  # TikTok's color
            )
            embed.add_field(
                name="Notifications",
                value=f"Live alerts will be sent to {live_now_channel.mention}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info(f"Added TikTok channel: {username}")
        else:
            await interaction.response.send_message(
                "❌ Could not verify this TikTok account. Please check the username and try again.",
                ephemeral=True
            )
    except Exception as e:
        logging.error(f"Error adding TikTok channel: {str(e)}")
        await interaction.response.send_message(
            "❌ Error processing TikTok channel. Please check the username format.",
            ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(add_tiktok)
