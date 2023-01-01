from discord.ext import commands
from discord import ApplicationContext
from discord.commands import slash_command
from discord.commands import Option
import random

from views.ButtonViews import GeneralView
from cog_helpers import random_helper
from config import TYPES

class RandomMiscSlash(commands.Cog):

    """Random Pokemon"""

    @slash_command(name="random_pokemon", description="Shows a randomly chosen pokemon")
    async def random_pokemon(self, ctx:ApplicationContext):
        poke = await random_helper.get_random_poke()
        reply = await random_helper.get_random_pokemon_embed(poke)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """Random Team"""

    @slash_command(name="random-team", description="Returns a random team from the tier")
    async def random_team(self, ctx:ApplicationContext, tier:Option(str, description="Enter the tier like common, mega, rare", required=True)):

        reply = await random_helper.get_random_team_embed(tier)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """Random Matchup"""

    @slash_command(name="random-matchup", description="Returns a random matchup from the tier")
    async def random_matchup(self, ctx:ApplicationContext, tier:Option(str, description="Enter the tier like common, mega, rare", required=True)):

        reply = await random_helper.get_random_matchup_embd(tier)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """Random Type"""

    @slash_command(name="random-type", description="Returns a random type for random battling")
    async def random_type(self, ctx:ApplicationContext):

        random_type = TYPES[random.randint(0, len(TYPES) - 1)]
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(f"HMMMMM! You got `{random_type.capitalize()}` type :3", view=view)
    

def setup(bot:commands.Bot):
    bot.add_cog(RandomMiscSlash())