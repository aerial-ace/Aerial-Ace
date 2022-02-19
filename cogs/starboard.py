from discord.ext import commands
from discord import TextChannel

from cog_helpers import starboard_helper

class StarboardSystem(commands.Cog):

    """Toggle Starboard Module"""

    @commands.command(name="starboard", aliases=["sb"])
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def starboard(self, ctx : commands.Context, channel:TextChannel = None):
        reply = await starboard_helper.set_starboard(str(ctx.guild.id), channel)

        await ctx.reply(reply)

def setup(bot : commands.Bot):
    bot.add_cog(StarboardSystem())