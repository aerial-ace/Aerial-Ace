from discord.ext import commands
from discord import Bot, Intents
import discord
import sys

from managers import cache_manager, mongo_manager, init_manager, post_command_manager
from config import TOKEN, MONGO_URI, TEST_TOKEN

from cog_helpers import general_helper

from checkers import rare_catch_detection
from checkers import auto_battle_log

# determines whether to run the bot in local, or global mode
is_test = False

intents = Intents.default()
intents.message_content = True

# for getting the prefix
def prefix_callable(bot : Bot, message):
    return [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> ", "-aa ", "aa."]

bot = commands.AutoShardedBot(command_prefix=prefix_callable, description="Botto", case_insensitive=True, intents=intents)
bot.remove_command("help")

initial_cogs = [
    "presence_cycle",
    "admin",
    "starboard",
    "help",
    "smogon",
    "mail",
    "utility",
    "suggestion",
    "error_handler",
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
    "suggestion",
    "tag",
    "smogon",
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
    mongo_manager.init_mongo(MONGO_URI, "aerialace")
    await cache_manager.cache_data()
    print(f"Logged in as {bot.user}")
    print(f"Discord Version : {discord.__version__}")

@bot.event
async def on_message(message:discord.Message):

    if message.author == bot.user :
        return

    # reply to solo pings
    if message.content == "<@908384747393286174>":
        await message.channel.send(embed=(await general_helper.get_info_embd(title="Alola :wave:, This is Aerial Ace.", desc="Prefix : `-aa` or `aa.`\n**Slash Commands are available**\nPing : **{ping} ms** \nHelp Command : `-aa help`".format(ping=round(bot.latency * 1000, 2)))))

    # detect rare catches from the poketwo bot
    await rare_catch_detection.rare_check(message)

    await auto_battle_log.determine_battle_message(bot, message)

    # process commands
    await bot.process_commands(message)

@bot.listen("on_command_completion")
@bot.listen("on_application_command_completion")
async def after_command(ctx : commands.Context):
    if ctx.command.name != "help" and ctx.command.name != "mail":
        await post_command_manager.process_post_commands(ctx)

def main():
    for cog in initial_cogs:
        bot.load_extension(f"cogs.{cog}")

    for slash_cog in initial_slash_cogs:
        bot.load_extension(f"cogs.slash.{slash_cog}")

if __name__ == "__main__":

    if len(sys.argv) < 2:
        is_test = False
    else:
        is_test = (True if sys.argv[1].lower() == "true" else False) 

    main()

    if is_test is False:
        bot.run(TOKEN)
    else:
        bot.run(TEST_TOKEN)
