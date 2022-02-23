import random
from discord.ext import commands

from cog_helpers import random_helper
from config import TYPES

class RandomMisc(commands.Cog):
    
    """View random pokemon"""

    @commands.guild_only()
    @commands.command(name="random_poke", aliases=["rp"])
    async def random_poke(self, ctx):
        
        reply = await random_helper.get_random_pokemon_embed()

        await ctx.send(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(RandomMisc())