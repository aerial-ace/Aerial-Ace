from discord.ext import commands
from discord import ApplicationContext
from discord.commands import slash_command
from discord.commands import Option
import random

from cog_helpers import random_helper
from config import TYPES

class RandomMiscSlash(commands.Cog):

    """Random Pokemon"""

    @slash_command(name="random_pokemon", description="Shows a randomly choosen pokemon", guild_ids=[751076697884852389])
    async def random_pokemon(self, ctx:ApplicationContext):
        poke = await random_helper.get_random_poke()
        reply = await random_helper.get_random_pokemon_embed(poke)

        await ctx.respond(embed=reply)

    """Random Team"""

    @slash_command(name="random-team", description="Returns a random team from the tier", guild_ids=[751076697884852389])
    async def random_team(self, ctx:ApplicationContext, tier:Option(str, description="Enter the tier like common, mega, rare", required=True)):

        reply = await random_helper.get_random_team_embed(tier)

        await ctx.respond(embed=reply)

    """Random Matchup"""

    @slash_command(name="random-matchup", description="Returns a random matchup from the tier", guild_ids=[751076697884852389])
    async def random_matchup(self, ctx:ApplicationContext, tier:Option(str, description="Enter the tier like common, mega, rare", required=True)):

        reply = await random_helper.get_random_matchup_embd(tier)

        await ctx.respond(embed=reply)

    """Random Type"""

    @slash_command(name="random-type", description="Returns a random type for random battling", guild_ids=[751076697884852389])
    async def random_type(self, ctx:ApplicationContext):

        random_type = TYPES[random.randint(0, len(TYPES) - 1)]

        await ctx.respond(f"HMMMMM! You got `{random_type.capitalize()}` type :3")
    

def setup(bot:commands.Bot):
    bot.add_cog(RandomMiscSlash())