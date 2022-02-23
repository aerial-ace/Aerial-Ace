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

    """Get Random Team"""

    @commands.command(name="random_team", aliases=["rand_team"])
    @commands.guild_only()
    async def get_random_team(self, ctx : commands.Context, tier):
        reply = await random_helper.get_random_team_embed(tier.lower())

        await ctx.reply(embed=reply)

    @get_random_team.error
    async def get_random_team_handler(self, ctx : commands.Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Give a Team Tier like ```{ctx.prefix}random_team mega```")
        else:
            await ctx.reply(error)

    """Get random matchup"""

    @commands.command(name="random_matchup", aliases=["rand_matchup"])
    @commands.guild_only()
    async def get_random_matchup(self, ctx : commands.Context, tier):
        reply = await random_helper.get_random_matchup_embd(tier.lower())

        await ctx.reply(embed=reply)

    @get_random_matchup.error
    async def get_random_matchup_handler(self, ctx:commands.Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"Give a Team Tier like ```{ctx.prefix}random_matchup mega```")
        else:
            await ctx.reply(error)

    """Get random type"""    
    
    @commands.command(name="random_type", aliases=["rand_type"])
    @commands.guild_only()
    async def get_random_type(self, ctx:commands.Context):
        random_type = TYPES[random.randint(0, len(TYPES) - 1)]

        await ctx.reply(f"HMMMMM! You got `{random_type.capitalize()}` type :3")

    @get_random_type.error
    async def get_random_type_handler(self, ctx:commands.Context, error):
        await ctx.reply(error)

def setup(bot : commands.Bot):
    bot.add_cog(RandomMisc())