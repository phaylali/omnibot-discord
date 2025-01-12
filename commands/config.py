import discord
from discord import app_commands
from utils.config_manager import ConfigManager

config_manager = ConfigManager()

@app_commands.command(
    name="config",
    description="Configure bot settings"
)
@app_commands.default_permissions(administrator=True)
@app_commands.choices(action=[
    app_commands.Choice(name="add_status_channel", value="add"),
    app_commands.Choice(name="remove_status_channel", value="remove"),
    app_commands.Choice(name="list_status_channels", value="list")
])
async def config(
    interaction: discord.Interaction,
    action: str,
    channel: discord.TextChannel = None
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need administrator permissions to use this command!", ephemeral=True)
        return

    if action == "add" and channel:
        if config_manager.add_status_channel(channel.id):
            await interaction.response.send_message(f"Added {channel.mention} to status notification channels!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} is already a status channel!", ephemeral=True)
    
    elif action == "remove" and channel:
        if config_manager.remove_status_channel(channel.id):
            await interaction.response.send_message(f"Removed {channel.mention} from status notification channels!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{channel.mention} is not a status channel!", ephemeral=True)
    
    elif action == "list":
        channels = config_manager.get_status_channels()
        if channels:
            channel_mentions = [f"<#{channel_id}>" for channel_id in channels]
            await interaction.response.send_message(f"Status notification channels:\n{', '.join(channel_mentions)}", ephemeral=True)
        else:
            await interaction.response.send_message("No status notification channels configured!", ephemeral=True)

async def setup(bot):
    bot.tree.add_command(config)
