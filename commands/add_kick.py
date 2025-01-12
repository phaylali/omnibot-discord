
import discord
from discord import app_commands
import logging

@app_commands.command(
    name="add-kick",
    description="Add a Kick channel to monitor"
)
async def add_kick(
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
        is_live, channel_data = await interaction.client.kick_monitor.check_live_status(channel_name)
        
        if channel_data:
            live_now_channel = discord.utils.get(interaction.guild.channels, name="live-now")
            await interaction.client.kick_monitor.monitor_channel(
                channel_name,
                live_now_channel.id
            )
            
            embed = discord.Embed(
                title="Kick Channel Added",
                description=f"Successfully added {channel_name} to monitoring",
                color=discord.Color.green()  # Kick's brand color
            )
            embed.add_field(
                name="Notifications",
                value=f"Live alerts will be sent to {live_now_channel.mention}"
            )
            embed.set_footer(text="Kick.com Integration")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info(f"Added Kick channel: {channel_name}")
        else:
            await interaction.response.send_message(
                "❌ Could not verify this Kick channel. Please check the channel name and try again.",
                ephemeral=True
            )
    except Exception as e:
        logging.error(f"Error adding Kick channel: {str(e)}")
        await interaction.response.send_message(
            "❌ Error processing Kick channel. Please check the channel name format.",
            ephemeral=True
        )

async def setup(bot):
    bot.tree.add_command(add_kick)
