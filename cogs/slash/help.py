from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import help_helper

class HelpSystemSlash(commands.Cog):
    
    @slash_command(name="help", description="Get help for a command/catagory")
    async def help(self, ctx : ApplicationContext, category : Option(str, description="Pick category to see commands", required=False, default=None)):

        if category is None:
            reply = await help_helper.get_help_embed(None)
            await ctx.respond(embed=reply)
        else:
            reply = await help_helper.get_category_help_embed(ctx=None, category=category.lower())
            await ctx.respond(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(HelpSystemSlash())