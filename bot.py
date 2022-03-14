from discord.ext import commands
from discord import Bot, Intents
import discord

from managers import cache_manager
from managers import mongo_manager
from managers import init_manager
from cogs import mail as mail_manager
from config import TOKEN, MONGO_URI, TEST_TOKEN, ADMIN_ID

from checkers import rare_catch_detection

# determines whether to run the bot in local, or global mode
is_test = False

intents = Intents.default()
intents.message_content = True

# for getting the prefix
def prefix_callable(bot : Bot, message):
    return [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> ", "-aa ", "aa."]

bot = commands.Bot(command_prefix=prefix_callable, description="Botto", case_insensitive=True, intents=intents)
bot.remove_command("help")

initial_cogs = [
    "presence_cycle",
    "admin",
    "starboard",
    "help",
    "mail",
    "utility",
    "pokedex",
    "pokemon_info",
    "random_misc",
    "tag",
    "fun",
    "battle"
]

initial_slash_cogs = [
    "pokedex",
    "pokeinfo",
    "starboard",
    "random_misc",
    "tag",
    "utility",
    "battle",
    "fun",
    "help"
]

@bot.event
async def on_guild_join(guild):
    await init_manager.register_guild(bot, guild)

@bot.event 
async def on_guild_remove(guild):
    await init_manager.remove_guild(bot, guild)

@bot.event
async def on_ready():
    await mongo_manager.init_mongo(MONGO_URI, "aerialace")
    await cache_manager.cache_data()
    print(f"Logged in as {bot.user}")
    print(f"Discord Version : {discord.__version__}")

@bot.event
async def on_message(message):

    if message.author == bot.user :
        return

    if message.content == "alola":
        await message.channel.send("You said, ALola")

    # detect rare catches from the poketwo bot
    await rare_catch_detection.rare_check(message)

    # process commands
    await bot.process_commands(message)

@bot.listen("on_command_completion")
async def after_command(ctx : commands.Context):
    if ctx.command.name != "help" and ctx.command.name != "mail":
        await mail_manager.process_mail(ctx)

@property
def starboard():
    return bot.get_cog("Starboard").instance

def main():
    for cog in initial_cogs:
        bot.load_extension(f"cogs.{cog}")

    for slash_cog in initial_slash_cogs:
        bot.load_extension(f"cogs.slash.{slash_cog}")

if __name__ == "__main__":
    main()

    if is_test is False:
        bot.run(TOKEN)
    else:
        bot.run(TEST_TOKEN)
