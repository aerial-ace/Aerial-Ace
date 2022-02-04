import discord
from discord.ext import commands

from managers import cache_manager
from cog_helpers import pokemon_info_helper

all_types = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

class Weakness(commands.Cog):

    """Weakness data Manager"""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="weakness", aliases=["weak"])
    async def get_weakness(self, ctx, *params):

        reply = await pokemon_info_helper.get_weakness_embed(params)

        await ctx.send(embed=reply)

def setup(bot):
    bot.add_cog(Weakness(bot))