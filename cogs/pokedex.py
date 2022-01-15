from discord.ext import commands

import config
from cog_helpers import pokedex_helper
from cog_helpers import general_helper

class PokeDex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dex(self, ctx, poke):

        try:
            poke_data = await pokedex_helper.get_poke_by_id(poke)
        except:
            reply = await general_helper.get_info_embd("Pokemon not found", f"Dex entry for id : `{poke}` was not found in the pokedex.\n Most uncommon ids follow this format : \n```-aa dex gallade-mega\n-aa dex meowstic-female\n-aa dex deoxys-defense\n-aa dex necrozma-dawn\n-aa dex calyrex-shadow-rider\n-aa dex cinderace-gmax```\nIf you still think this pokemon is missing, report it at official server", config.ERROR_COLOR)
            await ctx.send(embed=reply)
            return

        reply = await pokedex_helper.get_dex_entry_embed(poke_data)

        await ctx.send(embed=reply)

    @dex.error
    async def dex_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(":no: Give a pokemon name or id as a parameter")
        else:
            print(error)


def setup(bot):
    bot.add_cog(PokeDex(bot))