from discord.ext import commands

from cog_helpers import utility_helper
from cog_helpers import general_helper
import config

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

    @commands.command(name="support_server", aliases=["ss"])
    async def support_server(self, ctx):
        reply = await general_helper.get_info_embd("Support Server Links", f"To join support server, use this [link]({config.SUPPORT_SERVER_LINK})", color=config.NORMAL_COLOR, show_tumbnail=True)
        await ctx.send(embed=reply)

    @commands.command(name="about")
    async def about(self, ctx):
        reply = await utility_helper.get_about_embed()
        await ctx.send(embed=reply)

    @commands.command(name="vote")
    async def vote(self, ctx):
        reply = await utility_helper.get_vote_embed()
        await ctx.send(embed=reply)

    @commands.command(name="invite", aliases=["inv"])
    async def invite(self, ctx):
        reply = await utility_helper.get_support_server_embed()
        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(Utility(bot))