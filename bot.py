import sys

import discord
from discord import AutoShardedBot, Intents
from discord.ext import commands

from checkers import rare_catch_detection, spawn_speed_detection
from config import MONGO_URI, TEST_TOKEN, TOKEN
from helpers import general_helper
from managers import cache_manager, init_manager, logging_manager, mongo_manager, post_command_manager

logging_manager.setup_logging()
logger = logging_manager.main_logger

# determines whether to run the bot in local, or global mode
is_test = False

intents = Intents.default()
intents.message_content = True


# for getting the prefix
def prefix_callable(_bot: AutoShardedBot):
    if _bot.user is None:
        return ["-aa", "aa."]
    return [f"<@{_bot.user.id}> ", f"<@!{_bot.user.id}> ", "-aa ", "aa."]


bot = commands.AutoShardedBot(command_prefix=["-aa", "aa."], description="Botto", case_insensitive=True, intents=intents)
bot.command_prefix = prefix_callable(bot)

_ = bot.remove_command("help")

initial_cogs = ["presence_cycle", "admin", "starboard", "help", "smogon", "mail", "utility", "suggestion", "error_handler", "pokedex", "pokemon_info", "random_misc", "ruleset", "spawn_speed", "tag", "fun", "battle"]

initial_slash_cogs = ["pokedex", "pokeinfo", "starboard", "random_misc", "ruleset", "suggestion", "tag", "smogon", "utility", "battle", "fun", "help"]


@bot.event
async def on_guild_join(guild: discord.Guild):
    _ = await init_manager.register_guild(bot, guild)


@bot.event
async def on_guild_remove(guild: discord.Guild):
    await init_manager.remove_guild(bot, guild)


@bot.event
async def on_ready():
    _ = mongo_manager.init_mongo(MONGO_URI, "aerialace")
    await cache_manager.cache_data()

    logger.info(f"Logged in as {bot.user}")
    logger.info(f"Discord Version : {discord.__version__}")

    print(f"Logged in as {bot.user}")
    print(f"Discord Version : {discord.__version__}")


@bot.event
async def on_message(message: discord.Message):
    # ignore your own stuff
    if message.author == bot.user:
        return

    # reply to solo pings
    if message.content == "<@908384747393286174>":
        _ = await message.channel.send(embed=(await general_helper.get_info_embd(title="Alola :wave:, This is Aerial Ace.", desc=f"Prefix : `-aa` or `aa.`\n**Slash Commands are available**\nPing : **{round(bot.latency * 1000, 2)} ms** \nHelp Command : `-aa help`")))

    # detect rare catches from the poketwo bot
    await rare_catch_detection.rare_check(bot, message)

    # NOTE: Auto Battle Logging is not working as of now
    # await auto_battle_log.determine_battle_message(bot, message)

    await spawn_speed_detection.detect_spawn(message)

    # NOTE:  Donation Logging Module has been disabled and not supported anymore
    # _ = await donation_detection.donation_check(bot, message)

    # process commands
    await bot.process_commands(message)


@bot.listen("on_command_completion")
@bot.listen("on_application_command_completion")
async def after_command(ctx: commands.Context[commands.Bot]):

    if ctx.command is None:
        return

    if ctx.command.name != "help" and ctx.command.name != "mail":  # pyright: ignore[reportUnknownMemberType]
        await post_command_manager.process_post_commands(ctx)


def main():
    for cog in initial_cogs:
        bot.load_extension(f"cogs.{cog}")

    for slash_cog in initial_slash_cogs:
        bot.load_extension(f"cogs.slash.{slash_cog}")


if __name__ == "__main__":
    print("""
          ___            _       _    ___           
         / _ \\          (_)     | |  / _ \\          
        / /_\\ \\ ___ _ __ _  __ _| | / /_\\ \\ ___ ___ 
        |  _  |/ _ \\ '__| |/ _` | | |  _  |/ __/ _ \\
        | | | |  __/ |  | | (_| | | | | | | (_|  __/
        \\_| |_/\\___|_|  |_|\\__,_|_| \\_| |_/\\___\\___|
          
    """)

    if len(sys.argv) < 2:
        is_test = False
    else:
        is_test = sys.argv[1].lower() == "true"

    main()

    if is_test is False:
        bot.run(TOKEN)
    else:
        bot.run(TEST_TOKEN)
