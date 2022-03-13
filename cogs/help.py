from discord.ext import commands

from cog_helpers import help_helper

class HelpCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="help", aliases=["h"])
    async def send_help(self, ctx, category=None):

        print("Help Sent")

        if category is None:
            reply = await help_helper.get_help_embed(ctx)
            await ctx.send(embed=reply)
            return
        else:
            reply = await help_helper.get_category_help_embed(ctx, category.lower())
            await ctx.send(embed=reply)
            return

def setup(bot):
    bot.add_cog(HelpCommand(bot))