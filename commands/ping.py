import discord
from discord import app_commands

# Command group for organization (optional)
@app_commands.command(
    name="ping",
    description="Check the bot's latency"
)
async def ping(interaction: discord.Interaction):
    # Calculate and send the bot's latency
    latency = round(interaction.client.latency * 1000)
    await interaction.response.send_message(f"Pong! 🏓 Latency: {latency}ms")

# Setup function to add the command to the bot
async def setup(bot):
    bot.tree.add_command(ping)
