import os
import random
import re
import discord
import aiohttp
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

# Intents: message_content is required for reading message text
intents = discord.Intents.default()
intents.message_content = True

# Use commands.Bot so we can create prefix commands (recommended)
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
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
    

STATUS = "x_x" # only let me set it
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

@bot.tree.command(name="tutorial", description="Host your own app")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def tutorial(interaction: discord.Interaction):
    await interaction.response.send_message("https://alzox.carrd.co")
    return

@bot.tree.command(name="hello_world", description="Hello World!")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def hello_world(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World!")
    return 

@bot.tree.command(name="wikipedia", description="Returns main result for a wikipedia search")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def wikipedia(interaction: discord.Interaction, topic: str):
    await interaction.response.defer() # acknowledge but await for request to finish
    
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")
        headers = {
            'User-Agent': 'DiscordBot/1.0 (Discord Wikipedia Bot; Python/aiohttp)'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    title = data.get("title", "No title")
                    extract = data.get("extract", "No summary available")
                    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
                    
                    embed = discord.Embed(
                        title=title,
                        description=extract[:300] + ("..." if len(extract) > 300 else ""),
                        color=discord.Color.blue(),
                        url=page_url
                    )
                    
                    if "thumbnail" in data:
                        embed.set_thumbnail(url=data["thumbnail"]["source"])
                    await interaction.followup.send(embed=embed)
                elif response.status == 403:
                    await interaction.followup.send(f"403 blockedd")
                else:
                    await interaction.followup.send(f"{response.status}")
    except Exception as e:
        await interaction.followup.send(f"something bad has happened") 

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
