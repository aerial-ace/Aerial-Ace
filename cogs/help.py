from discord.ext import commands

from cog_helpers import help_helper
from views.GeneralView import GeneralView

class HelpCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="help", aliases=["h"])
    async def send_help(self, ctx, input=None,):

        view = GeneralView(200, True, True, True, True)

        if input is None:
            reply = await help_helper.get_help_embed(ctx)
            await ctx.send(embed=reply, view=view)
        else:
            reply = await help_helper.get_catagory_help_embed(ctx, input.lower())
            await ctx.send(embed=reply, view=view)

def setup(bot):
    bot.add_cog(HelpCommand(bot))