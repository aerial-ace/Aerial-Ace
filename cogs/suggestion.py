from discord.ext import commands

from views.ButtonViews import GeneralView
from cog_helpers import suggestion_helper

class SuggestionManager(commands.Cog):

    @commands.command(name="suggest", aliases=["review"], description="Sends your suggestion to the devs")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def register_suggestion(self, ctx:commands.Context, *suggestion):

        if len(suggestion) <= 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("Give Suggestion too :|")

        reply = await suggestion_helper.send_suggestion(ctx.guild, ctx.author, " ".join(suggestion))
        view = GeneralView(200, True, True, False, True)

        await ctx.reply(reply, view=view)

def setup(bot:commands.Bot):
    bot.add_cog(SuggestionManager())