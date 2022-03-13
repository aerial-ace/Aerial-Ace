from discord.ext import commands
from discord.ui import View, Button
from discord import ButtonStyle

from config import POKEMON_LINK_TEMPLATE_SMOGON, ABILITY_LINK_TEMPLATE_SMOGON, ERROR_COLOR
from cog_helpers import pokedex_helper
from cog_helpers import general_helper

class PokeDex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """View dex entry of any pokemon"""

    @commands.command(name="dex", aliases=["d"])
    @commands.guild_only()
    async def dex(self, ctx, poke):

        try:
            poke_data = await pokedex_helper.get_poke_by_id(poke)
        except:
            reply = await general_helper.get_info_embd("Pokemon not found", f"Dex entry for id : `{poke}` was not found in the pokedex.\n Most uncommon ids follow this format : \n```-aa dex gallade-mega\n-aa dex meowstic-female\n-aa dex deoxys-defense\n-aa dex necrozma-dawn\n-aa dex calyrex-shadow-rider\n-aa dex cinderace-gmax```\nIf you still think this pokemon is missing, report it at official server", ERROR_COLOR)
            await ctx.send(embed=reply)
            return

        reply = await pokedex_helper.get_dex_entry_embed(poke_data)

        view = View()
        view.add_item(Button(label="Comp. Guide", url=POKEMON_LINK_TEMPLATE_SMOGON.format(pokemon=poke), style=ButtonStyle.link))

        await ctx.send(embed=reply, view=view)

    @dex.error
    async def dex_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd(title="Error!!", desc="Please provide a `Pokemon_Name` or `Pokemon_ID` as a parameter", footer="Try [dex necrozma-dawn", color=ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

    """Check Abilities"""
    @commands.command(name="ability", aliases=["ab"])
    @commands.guild_only()
    async def ability(self, ctx:commands.Context, name):
        
        view = View()
        reply = await pokedex_helper.get_ability_embed(name)

        view.add_item(Button(label="Learn More", url=ABILITY_LINK_TEMPLATE_SMOGON.format(ability=name), style=ButtonStyle.link))

        await ctx.send(embed=reply, view=view)


def setup(bot):
    bot.add_cog(PokeDex(bot))