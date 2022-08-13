from discord.ext import commands
from discord import HTTPException

from views.ButtonViews import GeneralView

class ErrorHandler(commands.Cog):
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):

        cog:commands.Cog = ctx.cog
        view = GeneralView(200, True, True, False, True)

        # return if cog has its own handler
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        # exceptions that don't need to handled
        ignored_exceptions = (commands.CommandNotFound, )

        error = getattr(error, "original", error)    

        # return if error is one from ignored exceptions
        if isinstance(error, ignored_exceptions):
            return

        if isinstance(error, commands.DisabledCommand):
            return await ctx.reply("This command is currently disabled due to some reasons.", view=view)

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(f"Woah there!! You are on cooldown for this command. Try again in {round(error.retry_after, 2)} seconds", view=view)

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.reply("This command can not be used in DMs", view=view)
            except HTTPException:
                pass

        if isinstance(error, commands.NotOwner):
            return await ctx.reply("You are not supposed to use this command :>", view=view)

        await ctx.reply("Error Occurred ```{}```".format(error), view=view)
    

def setup(bot:commands.Bot):
    bot.add_cog(ErrorHandler())