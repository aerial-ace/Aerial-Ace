from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import help_helper
from views.GeneralView import GeneralView

class HelpSystemSlash(commands.Cog):
    
    @slash_command(name="help", description="Get help for a command", guild_ids=[751076697884852389])
    async def help(self, ctx : ApplicationContext, input : Option(str, description="Command to get help for", required=False, default=None)):

        view = GeneralView(200, True, True, True, True)

        if input is None:
            reply = await help_helper.get_help_embed(None)
            await ctx.respond(embed=reply, view=view)
        else:
            reply = await help_helper.get_category_help_embed(ctx=None, input=input.lower())
            await ctx.respond(embed=reply, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(HelpSystemSlash())