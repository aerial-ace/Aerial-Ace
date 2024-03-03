from discord.ext import commands
from discord.ext import tasks
from discord.abc import GuildChannel
from discord import TextChannel, VoiceChannel, StageChannel

from managers import cache_manager
from managers import mongo_manager

from checkers import spawn_speed_detection

class SpawnSpeedModule(commands.Cog):
    
    bot:commands.Bot = None

    def __init__(self, bot):
        self.bot = bot
        self.update_spawn_speeds.start()

    def cog_unload(self) -> None:
        self.update_spawn_speeds.cancel()

    @tasks.loop(hours=1)
    async def update_spawn_speeds(self):

        if cache_manager.cached_spawnrate_data is None:
            return

        await self.apply_spawn_counter()

        await self.apply_shiny_counter()

    @update_spawn_speeds.before_loop
    async def waiter(self):
        await self.bot.wait_until_ready()

    async def apply_spawn_counter(self, server_id:str=None):
        """ Updates the spawn-speed channel name of each and every server """

        d = cache_manager.cached_spawnrate_data.items()

        if server_id != None:
            d = [{server_id: cache_manager.get(server_id)}]

        for x, y in d:

            if y.get("active") is False:
                continue

            spawn_speed = await spawn_speed_detection.get_server_spawn_speed(str(x))

            try:
                speed_display_channel:GuildChannel = await self.bot.fetch_channel(y.get("channel_id"))
            except:
                continue # Channel Not Found

            if isinstance(speed_display_channel, TextChannel) or isinstance(speed_display_channel, VoiceChannel) or isinstance(speed_display_channel, StageChannel):
                try:
                    await speed_display_channel.edit(name=f"{spawn_speed} spawns / hour")
                    await spawn_speed_detection.reset_spawns(x)
                except:
                    continue # Unable to send messages.

    async def apply_shiny_counter(self, server_id:str=None):
        """ Updates the shiny-counter channel name of each and every server """

        d = cache_manager.cached_shinycounter_data.items()

        if server_id != None:
            d = [{server_id: cache_manager.get(server_id)}]

        for x, y in d:

            if y.get("active") is False:
                continue

            try:
                display_channel : GuildChannel = await self.bot.fetch_channel(int(y.get("channel_id")))
            except:
                continue

            if isinstance(display_channel, TextChannel) or isinstance(display_channel, VoiceChannel) or isinstance(display_channel, StageChannel):

                try:
                    await display_channel.edit(name="{} shinies / alltime".format(y.get("count")))
                except:
                    continue

    """ SPAWN COUNTER """

    @commands.group(name="spawnrate", aliases=["sr"], description="The container for spawnrate commands")
    async def spawnrate(self, context:commands.Context):
        if context.subcommand_passed is None:
            return await context.send("Please provide a valid subcommand")

    @commands.has_permissions(administrator=True)        
    @spawnrate.command(name="channel", aliases=["ch"], description="Set the spawn rate display channel")
    async def sr_channel(self, context:commands.Context, channel:GuildChannel):

        if channel is None:
            return await context.send("Please provide a valid channel!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), active=None, channel_id=str(channel.id))

        await context.send("SpawnRate Display Channel was set to " + channel.mention)

    @commands.has_permissions(administrator=True)
    @spawnrate.command(name="activate", aliases=["a"], description="Activate the spawn rate display")
    async def sr_activate(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up spawnrate channel before activating the module!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), True, channel_id=None)

        await context.send("SpawnRate Module was activated")

    @commands.has_permissions(administrator=True)
    @spawnrate.command(name="deactivate", aliases=["da"], description="DeActivate the spawn rate display")
    async def sr_deactivate(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up spawnrate channel before deactivating the module!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), False, channel_id=None)

        await context.send("SpawnRate Module was deactivated")

    @spawnrate.command(name="count", aliases=["c"], description="Current Spawn Count of the server")
    async def sr_spawn_count(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("No Data recorded")

        await context.send("Current Spawn Count : **{}**".format(str(await spawn_speed_detection.get_server_spawn_speed(str(context.guild.id)))))

    @spawnrate.command("apply", description="Applies the counter values of the current server.")
    @commands.is_owner()
    async def sr_apply(self, context:commands.Context, server_id:str=None):

        await self.apply_spawn_counter(server_id)

        await context.send("Spawn Counter Applied.")


    """ SHINY COUNTER """

    @commands.group(name="shiny-counter", aliases=["sc"], description="Commands related to shiny counter")
    async def shiny_counter(self, context:commands.Context):
        if context.subcommand_passed is None:
            await context.send("Please provide a valid subcommand!")

    @commands.has_permissions(administrator=True)
    @shiny_counter.command(name="channel", aliases=["ch"], description="Set the shiny count channel")
    async def sc_channel(self, context:commands.Context, channel:GuildChannel):

        if channel is None:
            return await context.send("Please provide a valid channel as parameter!")

        await mongo_manager.manager.update_shiny_counter(str(context.guild.id), None, str(channel.id))

        await context.send("Shiny Counter Channel Updated! New Shiny Counter Display : {}".format(channel.mention))

    @commands.has_permissions(administrator=True)
    @shiny_counter.command(name="activate", aliases=["a"], description="Activate the shiny counter display")
    async def sc_activate(self, context:commands.Context):

        data = cache_manager.cached_shinycounter_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up shiny counter channel before activating the module!")
        
        await mongo_manager.manager.update_shiny_counter(str(context.guild.id), True, channel_id=None)

        await context.send("ShinyCounter Module was activated")

    @commands.has_permissions(administrator=True)
    @shiny_counter.command(name="deactivate", aliases=["da"], description="DeActivate the shiny counter display")
    async def sc_deactivate(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up spawnrate channel before deactivating the module!")
        
        await mongo_manager.manager.update_shiny_counter(str(context.guild.id), False, channel_id=None)

        await context.send("ShinyCounter Module was deactivated")

    @shiny_counter.command(name="count", aliases=["c"], description="Current Shiny Counter of the server")
    async def sc_spawn_count(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("No Data recorded")

        await context.send("Current Shiny Count : **{}**".format(cache_manager.cached_shinycounter_data.get("count")))

    @commands.is_owner()
    @shiny_counter.command("apply", description="Applies the counter values of the current server.")
    async def sc_apply(self, context:commands.Context, server_id:str=None):

        await self.apply_shiny_counter(server_id)

        await context.send("Shiny Counter Applied.")

def setup(bot:commands.Bot):
    bot.add_cog(SpawnSpeedModule(bot))
