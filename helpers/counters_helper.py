from discord.ext import commands
from discord.abc import GuildChannel
from discord import TextChannel, VoiceChannel, StageChannel

from managers import cache_manager, mongo_manager

async def increment_shiny_counter(bot:commands.Bot, server_id):

    await mongo_manager.manager.increment_shiny_counter(str(server_id))

    

