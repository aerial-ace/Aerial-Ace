from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import help_helper
from views.GeneralView import GeneralView

class HelpSystemSlash(commands.Cog):
    
    @slash_command(name="help", description="Get help for a command/catagory")
    async def help(self, ctx : ApplicationContext, category : Option(str, description="Pick category to see commands", required=False, default=None)):

        if category is None:
            reply = await help_helper.get_help_embed(None)
            view = GeneralView(200, True, True, True, True)

            await ctx.respond(embed=reply, view=view)
        else:
            reply = await help_helper.get_category_help_embed(ctx=None, category=category.lower())
            view = GeneralView(200, True, True, True, True)

            await ctx.respond(embed=reply, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(HelpSystemSlash())