from discord.ext import commands

from cog_helpers import smogon_helper

class SmogonModule(commands.Cog):
    
    """Get Smogon Details of a pokemon"""

    @commands.command(name="smogon", aliases=["analyse"])
    async def smogon_details(self, ctx:commands.Context, tier:str, pokemon:str):
        
        await ctx.send("Param : " + pokemon)

        try:
            data = await smogon_helper.get_smogon_data(tier, pokemon)
        except Exception as e:
            return await ctx.reply("Wrong Pokemon Name ig\n" + "**Exit : ** {}".format(e))

        reply = await smogon_helper.get_smogon_embed(data)

        await ctx.send(embed=reply)

def setup(bot:commands.Bot):
    bot.add_cog(SmogonModule())