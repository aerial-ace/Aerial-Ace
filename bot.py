from discord.ext import commands

from managers import cache_manager
from managers import mongo_manager
from managers import init_manager
from cogs import mail as mail_manager
from config import TOKEN, MONGO_URI, TEST_TOKEN

from checkers import rare_catch_detection

is_test = True
test_prefix = "aa."

bot = commands.Bot(command_prefix=commands.when_mentioned_or("-aa "), description="Aerial Ace")
bot.remove_command("help")

initial_cogs = [
    "cogs.presence_cycle",
    "cogs.admin",
    "cogs.help",
    "cogs.mail",
    "cogs.utility",
    "cogs.pokedex",
    "cogs.pokemon_info",
    "cogs.tag",
    "cogs.weakness",
    "cogs.fun",
    "cogs.battle"
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

@bot.event
async def on_message(message):

    if message.author == bot.user :
        return

    # detect rare catches from the poketwo bot
    await rare_catch_detection.rare_check(message)

    # process commands
    await bot.process_commands(message)

@bot.listen("on_command_completion")
async def after_command(ctx : commands.Context):
    if ctx.command.name != "help" and ctx.command.name != "mail":
        await mail_manager.process_mail(ctx)

def main():
    for cog in initial_cogs:
        bot.load_extension(cog)

if __name__ == "__main__":
    main()

    if is_test is False:
        bot.run(TOKEN, bot=True, reconnect=True)
    else:
        bot.command_prefix = commands.when_mentioned_or(test_prefix)
        bot.run(TEST_TOKEN, bot=True, reconnect=True)