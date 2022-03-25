from discord.ext import commands
from discord import HTTPException

class ErrorHandler(commands.Cog):
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):

        if hasattr(ctx.command, "on_error"):
            return

        cog:commands.Cog = ctx.cog

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
            return await ctx.reply("This command is currently disabled due to some reasons.")

        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.reply("This command can not be used in DMs")
            except HTTPException:
                pass

        if isinstance(error, commands.NotOwner):
            return await ctx.reply("You are not supposed to use this command :>")

        await ctx.reply(error)
    

def setup(bot:commands.Bot):
    bot.add_cog(ErrorHandler())