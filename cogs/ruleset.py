from discord.ext import commands

from views.ButtonViews import GeneralView
from helpers import ruleset_helper

class RuleSetModule(commands.Cog):
    
    @commands.command(name="random_ruleset", aliases=["rrs", "rr"], description="Returns a bunch of random rules for pokemon battles.")
    async def random_ruleset(self, ctx:commands.Context):

        reply = await ruleset_helper.get_random_ruleset_embed()
        view  = GeneralView()

        await ctx.send(embed=reply, view=view)

    @commands.is_owner()
    @commands.command(name="add_ruleset", aliases=["ars"], description="Adds a ruleset to the Random Ruleset database.")
    async def add_ruleset(self, ctx:commands.Context, *details):

        details_parts = " ".join(details).split("|")

        print(details_parts)

        name = details_parts[0].strip()
        user = details_parts[-1].strip()
        rules = details_parts[1:-1]

        reply = await ruleset_helper.add_ruleset(name, rules, user)

        await ctx.reply(reply)

def setup(bot):
    bot.add_cog(RuleSetModule())
