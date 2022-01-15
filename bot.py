from discord.ext import commands

import config
from cog_helpers import cache_helper

bot = commands.Bot(command_prefix="[", description="Aerial Ace")

initial_cogs = [
    "cogs.pokedex"
]

@bot.event
async def on_ready():
    await cache_helper.cache_data()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    if message.author.id != int(config.ADMIN_ID):
        return

    await bot.process_commands(message)

def main():
    for cog in initial_cogs:
        bot.load_extension(cog)

TOKEN = config.TOKEN

if __name__ == "__main__":
    main()

    bot.run(TOKEN, bot=True, reconnect=True)