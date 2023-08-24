from discord.ext import commands
from discord import ApplicationContext
from discord.commands import slash_command

from views.ButtonViews import GeneralView
from helpers import ruleset_helper


class RuleSetSlashModule(commands.Cog):

    @slash_command(name="random-ruleset", description="Returns a bunch of random rules for pokemon battles.")
    async def random_ruleset(self, ctx: ApplicationContext):
        reply = await ruleset_helper.get_random_ruleset_embed()
        view = GeneralView()

        await ctx.respond(embed=reply, view=view)


def setup(bot):
    bot.add_cog(RuleSetSlashModule())
