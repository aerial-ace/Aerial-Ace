from discord.ext import commands

from cog_helpers import smogon_helper, general_helper
from config import ERROR_COLOR

class SmogonModule(commands.Cog):
    
    """Get Smogon Details of a pokemon"""

    @commands.command(name="smogon", aliases=["analyse"], description="Returns complete usage analysis of a pokemon from smogon database")
    async def smogon_details(self, ctx:commands.Context, gen:int, tier:str, pokemon:str):

        data = await smogon_helper.get_smogon_data(gen=gen, tier=tier, pokemon=pokemon)
        
        if data is None:
            return await general_helper.get_info_embd("Error", "Some Unknown Error occured while trying to fetch smogon data.", color=ERROR_COLOR)

        try:
            paginator = await smogon_helper.get_smogon_paginator(data)
            await paginator.send(ctx)
        except:
            await ctx.reply(embed=await general_helper.get_info_embd("Error!!", "**Error Code :** {code}\n**Error Description** {desc}\n\nThere is a possiblity that the searched pokemon is not available in that generation or in that tier. \nTry with gen it was first introduced in.".format(code=data.error, desc=data.message), color=ERROR_COLOR))

    @smogon_details.error
    async def smogon_details_handler(self, ctx:commands.Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Oh no!", f"This command requires these parameters \n```{ctx.prefix}smogon <gen> <tier> <pokemon>\n{ctx.prefix}smogon 5 OU tyranitar```", color=ERROR_COLOR, footer="Try /smogon too")
            await ctx.send(embed=reply)
        else:
            await ctx.reply(error)

def setup(bot:commands.Bot):
    bot.add_cog(SmogonModule())