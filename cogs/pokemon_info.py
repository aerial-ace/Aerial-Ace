from discord.ext import commands

import config
from cog_helpers import pokemon_info_helper
from cog_helpers import general_helper

class Pokemon_Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def stats(self, ctx, poke:str):
        reply = await pokemon_info_helper.get_stats_embed(poke)
        await ctx.send(embed=reply)

    @stats.error
    async def stats_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", "A pokemon name is required for this command. Try this ```>>stats Solgaleo```", config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

    @commands.guild_only()
    @commands.command(name="moveset", aliases=["ms"])
    async def moveset(self, ctx, poke : str):
        reply = await pokemon_info_helper.get_moveset_embed(poke)
        await ctx.send(embed=reply)

    @moveset.error
    async def moveset_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", "A pokemon name is required for this command, try this ```>>moveset Zekrom```", config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

    @commands.guild_only()
    @commands.command()
    async def nature(self, ctx, poke : str):
        reply = await pokemon_info_helper.get_nature_embed(poke)
        await ctx.send(embed=reply)

    @nature.error
    async def nature_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Gib pokemon name as a param when :/", "A pokemon name is required for this command, try this ```>>nature Nihilego```", config.ERROR_COLOR)
            await ctx.send(embed=reply)
        else:
            await ctx.send(error)

def setup(bot):
    bot.add_cog(Pokemon_Info(bot))