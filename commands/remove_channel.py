import discord
from discord import app_commands

class RemoveChannelCog:
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command(
        name="remove_channel",
        description="Removes a specified channel from the server"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def remove_channel(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        reason: str = "No reason provided"
    ):
        try:
            await channel.delete(reason=reason)
            await interaction.response.send_message(f"Channel {channel.name} has been successfully removed.\nReason: {reason}")
        except discord.Forbidden:
            await interaction.response.send_message("I don't have permission to delete that channel.")
        except discord.NotFound:
            await interaction.response.send_message("That channel was not found.")
        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}")

async def setup(bot):
    bot.tree.add_command(RemoveChannelCog(bot).remove_channel)
