import discord
from discord import app_commands

class StreamCog:
    def __init__(self, bot):
        self.bot = bot
        self.tree = bot.tree

    @app_commands.command(
        name="stream",
        description="Set your streaming status with a custom message"
    )
    async def stream(
        self,
        interaction: discord.Interaction,
        title: str,
        url: str,
        platform: str = "Twitch"
    ):
        try:
            streaming_activity = discord.Streaming(
                name=title,
                url=url,
                platform=platform
            )
            
            await self.bot.change_presence(activity=streaming_activity)
            
            embed = discord.Embed(
                title="🎮 Streaming Status Updated",
                description=f"Now streaming: {title}",
                color=discord.Color.purple()
            )
            embed.add_field(name="Platform", value=platform, inline=True)
            embed.add_field(name="URL", value=url, inline=True)
            
            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            await interaction.response.send_message(f"Failed to set streaming status: {str(e)}")

async def setup(bot):
    bot.tree.add_command(StreamCog(bot).stream)