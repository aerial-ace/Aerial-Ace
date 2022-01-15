from distutils import errors
from discord.ext import commands

from cog_helpers import utility_helper

class Utility(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def roll(self, ctx, max_value : int = 100):
        reply = await utility_helper.roll(max_value, ctx.author)
        await ctx.send(reply)

    @roll.error
    async def roll_handler(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.reply("Gib a interger as an argument like `>>roll 69`")
        else:
            await ctx.reply(error)

def setup(bot):
    bot.add_cog(Utility(bot))