import discord
from discord import Intents
from discord.ext import commands

from checkers import rare_catch_detection, spawn_speed_detection
from config import MONGO_URI
from helpers import general_helper
from managers import cache_manager, init_manager, mongo_manager, post_command_manager
from managers.logging_manager import get_logger

logger = get_logger("main")

# determines whether to run the bot in local, or global mode
is_test = False

intents = Intents.default()
intents.message_content = True


class AerialAce(commands.AutoShardedBot):
    def __init__(self):
        self.setup_done = False
        self.initial_cogs = ["presence_cycle", "admin", "starboard", "help", "smogon", "mail", "utility", "suggestion", "error_handler", "pokedex", "pokemon_info", "random_misc", "ruleset", "spawn_speed", "tag", "fun", "battle"]
        self.initial_slash_cogs = ["pokedex", "pokeinfo", "starboard", "random_misc", "ruleset", "suggestion", "tag", "smogon", "utility", "battle", "fun", "help"]

        super().__init__(command_prefix=self.prefix_callable, description="Botto", case_insensitive=True, intents=intents)
        _ = self.remove_command("help")

    # for getting the prefix
    def prefix_callable(self, bot, message):
        if bot.user is None:
            return ["-aa", "aa."]
        return [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> ", "-aa ", "aa."]

    async def load_cogs(self):
        for cog in self.initial_cogs:
            self.load_extension(f"cogs.{cog}")

        for slash_cog in self.initial_slash_cogs:
            self.load_extension(f"cogs.slash.{slash_cog}")

        logger.info("Cogs Loaded!")

    async def on_guild_join(self, guild: discord.Guild):
        if not self.setup_done:
            return

        _ = await init_manager.register_guild(self, guild)

        logger.info(f"Guild with name : {guild.name} and id {guild.id} joined!")

    async def on_guild_remove(self, guild: discord.Guild):
        if not self.setup_done:
            return

        await init_manager.remove_guild(self, guild)

        logger.info(f"Guild with name : {guild.name} and id {guild.id} removed!")

    async def connect(self, *, reconnect=True) -> None:
        if not self.setup_done:
            await self.do_setup()

        await super().connect(reconnect=True)

    async def do_setup(self):
        mongo_manager.init_mongo(MONGO_URI, "aerialace")
        await cache_manager.cache_data()
        await self.load_cogs()
        self.add_listener(self.after_command, "on_command_completion")
        self.add_listener(self.after_command, "on_application_command_completion")

        """
        mongo_manager.init_mongo(MONGO_URI, "aerialace")
        await cache_manager.cache_data()

        await self.load_cogs()

        # Make sure the after commands are hitting
        self.add_listener(self.after_command, "on_command_completion")
        self.add_listener(self.after_command, "on_application_command_completion")
        """

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        logger.info(f"Discord Version : {discord.__version__}")

        print(f"Logged in as {self.user}")
        print(f"Discord Version : {discord.__version__}")

        self.setup_done = True

    async def on_message(self, message: discord.Message):
        if self.setup_done is False:
            return

        if message.author == self.user or message.content == "":
            return

        # reply to solo pings
        if message.content == "<@908384747393286174>":
            _ = await message.channel.send(embed=(await general_helper.get_info_embd(title="Alola :wave:, This is Aerial Ace.", desc=f"Prefix : `-aa` or `aa.`\n**Slash Commands are available**\nPing : **{round(self.latency * 1000, 2)} ms** \nHelp Command : `-aa help`")))

        await rare_catch_detection.rare_check(self, message)
        await spawn_speed_detection.detect_spawn(message)

        # NOTE:  Battle and Donation Logging Modules have been disabled and not supported anymore for time being
        # await donation_detection.donation_check(self, message)
        # await auto_battle_log.determine_battle_message(self, message)

        await self.process_commands(message)

    async def after_command(self, ctx: commands.Context[commands.Bot]):
        if ctx.command is None:
            return

        if ctx.command.name != "help" and ctx.command.name != "mail":  # pyright: ignore[reportUnknownMemberType]
            await post_command_manager.process_post_commands(ctx)
