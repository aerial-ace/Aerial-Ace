from discord import TextChannel
from discord.ext import commands
from discord import ApplicationContext, Option
from discord.commands import slash_command

from cog_helpers import starboard_helper

class StarboardSlash(commands.Cog):

    """Enable or Disable the starboard channel"""

    @slash_command(name="starboard", description="Enable/Disable Starboard Channel")
    async def set_starboard(self, ctx:ApplicationContext, channel : Option(TextChannel, description="Channel where Rare Catches will be sent", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")
            
        reply = await starboard_helper.set_starboard(str(ctx.guild_id), channel)
        await ctx.respond(reply)


def setup(bot:commands.Bot):
    bot.add_cog(StarboardSlash())