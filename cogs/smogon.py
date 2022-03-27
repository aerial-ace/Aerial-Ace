from discord.ext import commands

from cog_helpers import smogon_helper, general_helper
from views.GeneralView import GeneralView
from config import ERROR_COLOR

class SmogonModule(commands.Cog):
    
    """Get Smogon Details of a pokemon"""

    @commands.command(name="smogon", aliases=["analyse"])
    async def smogon_details(self, ctx:commands.Context, gen:int, tier:str, pokemon:str):

        data = await smogon_helper.get_smogon_data(gen=gen, tier=tier, pokemon=pokemon)
        
        if data is None:
            return await general_helper.get_info_embd("Error", "Some Unknown Error occured while trying to fetch smogon data.", color=ERROR_COLOR)

        reply = await smogon_helper.get_smogon_embed(data)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

def setup(bot:commands.Bot):
    bot.add_cog(SmogonModule())