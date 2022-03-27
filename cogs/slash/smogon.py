from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Option

from cog_helpers import smogon_helper
from views.GeneralView import GeneralView

class SmogonSlashModule(commands.Cog):

    @slash_command(name="smogon", description="Smogon Analysis of the pokemon")
    async def smogon_slash(self, ctx:ApplicationContext, gen:Option(int, description="The Generation to look into"), tier:Option(str, description="Tier to look into"), pokemon:Option(str, description="Name of the pokemon", required=True)):

        data = await smogon_helper.get_smogon_data(gen=gen, tier=tier, pokemon=pokemon)
        reply = await smogon_helper.get_smogon_embed(data)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

def setup(bot:commands.Bot):
    bot.add_cog(SmogonSlashModule())