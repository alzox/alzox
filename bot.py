import os
import random
import re
import discord
from discord.ext import commands


TOKEN = os.getenv("DISCORD_TOKEN")

# Intents: message_content is required for reading message text
intents = discord.Intents.default()
intents.message_content = True

# Use commands.Bot so we can create prefix commands (recommended)
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (id: {bot.user.id})")
    await bot.tree.sync() # sync's auto fill commands
    print("Synced global app commands")

def _roll_notation_reply(notation: str) -> str:
    """Parse notation and return a reply string. Raises ValueError for invalid input."""
    notation = notation.strip().lower()
    m = re.fullmatch(r'(?:(\d*)d)?(\d+)', notation)
    if not m:
        raise ValueError("Invalid dice notation. Use NdM like 2d6, d20, or 6.")

    count_str, sides_str = m.group(1), m.group(2)
    if count_str is None:
        count = 1
    else:
        count = int(count_str) if count_str != "" else 1

    sides = int(sides_str)

    if count < 1 or count > 100:
        raise ValueError("Invalid number of dice. Please use 1-100 dice.")
    if sides < 2 or sides > 1000:
        raise ValueError("Invalid number of sides. Please use 2-1000 sides.")

    rolls = [random.randint(1, sides) for _ in range(count)]
    total = sum(rolls)

    if count == 1:
        return f"Rolled 1d{sides}: {rolls[0]}"
    return f"Rolled {count}d{sides}: {rolls} => total {total}"

@bot.tree.command(name="dice", description="Roll dice. Examples: 2d6, d20, 6")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slash_dice(interaction: discord.Interaction, notation: str = "1d6"):
    try:
        reply = _roll_notation_reply(notation)
    except ValueError as ve:
        await interaction.response.send_message(str(ve), ephemeral=True)
        return

    await interaction.response.send_message(reply)
    
STATUS = "" # only let me set it
@bot.tree.command(name="status", description="Check what @alzox is up to")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def status(interaction: discord.Interaction, status: str = "[status input]"):
    global STATUS
    if await bot.is_owner(interaction.user) and status != "[status input]":
        STATUS = status
        await interaction.response.send_message("Status Successfully Set!")
        return
    else:
        await interaction.response.send_message(STATUS)
        return

@bot.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("Missing required argument. Usage: !ask <your question>", mention_author=False)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(str(error), mention_author=False)
    else:
        print(f"Command error: {error}")
        await ctx.reply("An error occurred while processing your command.", mention_author=False)

if __name__ == "__main__":
    if not TOKEN:
        print("DISCORD_TOKEN not set. Set the DISCORD_TOKEN environment variable and try again.")
    else:
        bot.run(TOKEN)
