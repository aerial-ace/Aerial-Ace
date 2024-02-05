from discord.ext import commands
from discord.ext import tasks
from discord.abc import GuildChannel
from discord import TextChannel, VoiceChannel, StageChannel

import datetime

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

    @tasks.loop(hour=1)
    async def update_spawn_speeds(self):

        if cache_manager.cached_spawnrate_data is None:
            return

        for x, y in cache_manager.cached_spawnrate_data.items():

            if y.get("active") is False:
                continue

            spawn_speed = await spawn_speed_detection.get_server_spawn_speed(str(x))

            try:
                speed_display_channel:GuildChannel = await self.bot.fetch_channel(y.get("channel_id"))
            except:
                return # Channel Not Found

            if isinstance(speed_display_channel, TextChannel) or isinstance(speed_display_channel, VoiceChannel) or isinstance(speed_display_channel, StageChannel):
                try:
                    await speed_display_channel.edit(name=f"{spawn_speed} spawns / hour")
                    await spawn_speed_detection.reset_spawns(x)
                except:
                    continue # Unable to send messages.

    @update_spawn_speeds.before_loop
    async def waiter(self):
        await self.bot.wait_until_ready()





    @commands.has_permissions(administrator=True)
    @commands.group(name="spawnrate", aliases=["sr"], description="The container for spawnrate commands")
    async def spawnrate(self, context:commands.Context):
        if context.subcommand_passed is None:
            return await context.send("Please provide a valid subcommand")
        
    @spawnrate.command(name="channel", aliases=["ch"], description="Set the spawn rate display channel")
    async def channel(self, context:commands.Context, channel:GuildChannel):

        if channel is None:
            return await context.send("Please provide a valid channel!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), active=None, channel_id=str(channel.id))

        await context.send("SpawnRate Display Channel was set to " + channel.mention)

    @spawnrate.command(name="activate", aliases=["a"], description="Activate the spawn rate display")
    async def activate(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up spawnrate channel before activating the module!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), True, channel_id=None)

        await context.send("SpawnRate Module was activated")

    @spawnrate.command(name="deactivate", aliases=["da"], description="Activate the spawn rate display")
    async def deactivate(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("Please set up spawnrate channel before deactivating the module!")
        
        await mongo_manager.manager.update_spawnrate(str(context.guild.id), False, channel_id=None)

        await context.send("SpawnRate Module was deactivated")

    @spawnrate.command(name="count", description="Current Spawn Count of the server")
    async def spawn_count(self, context:commands.Context):

        data = cache_manager.cached_spawnrate_data.get(str(context.guild.id), None)

        if data is None:
            return await context.send("No Data recorded")
        
        await context.send(str(data.items()))
        await context.send(str(await spawn_speed_detection.get_server_spawn_speed(str(context.guild.id))))

def setup(bot:commands.Bot):
    bot.add_cog(SpawnSpeedModule(bot))
