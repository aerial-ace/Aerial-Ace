from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Option

from cog_helpers import smogon_helper

class SmogonSlashModule(commands.Cog):

    @slash_command(name="smogon", description="Smogon Analysis of the pokemon")
    async def smogon_slash(self, ctx:ApplicationContext, gen:Option(int, description="The Generation to look into"), tier:Option(str, description="Tier to look into"), pokemon:Option(str, description="Name of the pokemon", required=True)):

        data = await smogon_helper.get_smogon_data(gen=gen, tier=tier, pokemon=pokemon)
        paginator = await smogon_helper.get_smogon_paginator(data)

        await paginator.send(ctx)

def setup(bot:commands.Bot):
    bot.add_cog(SmogonSlashModule())