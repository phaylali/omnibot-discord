import discord
from discord import app_commands
import random

# Coin flip images
COIN_IMAGES = {
    "heads": "https://i.imgur.com/onRIi79.jpeg",  
    "tails": "https://i.imgur.com/4PPZu9Z.jpeg"   
}

WIN_MESSAGES = [
    "🎉 Congratulations! You're a master of prediction!",
    "🌟 Amazing guess! The odds were in your favor!",
    "✨ You've got the magic touch! Well done!",
    "🎯 Spot on! You should try the lottery next!",
    "🏆 Perfect prediction! You're on fire!"
]

LOSE_MESSAGES = [
    "😅 Better luck next time! The coin had other plans!",
    "🎲 Close call! Give it another shot!",
    "💫 The coin wasn't on your side this time!",
    "🍀 Don't worry, your luck will turn around!",
    "🌈 Almost had it! Try again!"
]

@app_commands.command(
    name="coinflip",
    description="Flip a coin and test your luck!"
)
@app_commands.choices(choice=[
    app_commands.Choice(name="heads", value="heads"),
    app_commands.Choice(name="tails", value="tails")
])
async def coinflip(interaction: discord.Interaction, choice: str):
    await interaction.response.defer()

    result = random.choice(["heads", "tails"])
    
    # Determine win/lose state and set appropriate indicators
    if choice == result:
        status_dots = "🟢 🟢 🟢 WIN 🟢 🟢 🟢"
        embed_color = discord.Color.green()
        message = random.choice(WIN_MESSAGES)
    else:
        status_dots = "🔴 🔴 🔴 LOSE 🔴 🔴 🔴"
        embed_color = discord.Color.red()
        message = random.choice(LOSE_MESSAGES)
    
    embed = discord.Embed(
        title=f"🎲 IT'S {result.upper()}! 🎲",
        description=f"{status_dots}\n\n{message}",
        color=embed_color
    )
    
    embed.add_field(
        name="Your Choice",
        value=choice.capitalize(),
        inline=True
    )
    
    embed.set_image(url=COIN_IMAGES[result])
    embed.set_footer(text=f"Flipped by {interaction.user.name}")
    
    await interaction.followup.send(embed=embed)

async def setup(bot):
    bot.tree.add_command(coinflip)
