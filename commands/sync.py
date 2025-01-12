import discord
from discord import app_commands

class SyncCog:
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command(
        name="sync",
        description="Syncs the command tree with Discord"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        await self.bot.tree.sync()
        await interaction.response.send_message("Commands synced successfully!")

async def setup(bot):
    bot.tree.add_command(SyncCog(bot).sync)
