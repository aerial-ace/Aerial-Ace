from discord.ext import commands

import config
from managers import cache_manager
from managers import mongo_manager
from managers import init_manager

from checkers import rare_catch_detection

bot = commands.Bot(command_prefix=">>", description="Aerial Ace")

initial_cogs = [
    "cogs.admin",
    "cogs.utility",
    "cogs.pokedex",
    "cogs.pokemon_info",
    "cogs.tag",
    "cogs.weakness",
    "cogs.battle"
]


@bot.event
async def on_guild_join(guild):
    init_manager.register_guild(bot, guild)

@bot.event 
async def on_guild_remove(guild):
    init_manager.remove_guild(bot, guild)

@bot.event
async def on_ready():
    await mongo_manager.init_mongo(config.MONGO_URI, "aerialace")
    await cache_manager.cache_data()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):

    await rare_catch_detection.rare_check(message)

    await bot.process_commands(message)

def main():
    for cog in initial_cogs:
        bot.load_extension(cog)

TOKEN = config.TOKEN

if __name__ == "__main__":
    main()

    bot.run(TOKEN, bot=True, reconnect=True)