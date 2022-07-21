from discord.ext import commands
from discord.ui import View, Button
from discord import ButtonStyle

from views.ButtonViews import GeneralView
from cog_helpers import pokedex_helper
from cog_helpers import general_helper
from config import POKEMON_LINK_TEMPLATE_SMOGON, ABILITY_LINK_TEMPLATE_SMOGON, ERROR_COLOR, INVITE_LINK

class PokeDex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """View dex entry of any pokemon"""

    @commands.command(name="dex", aliases=["d"], description="Pokedex for every pokemon")
    @commands.guild_only()
    async def dex(self, ctx, poke):

        try:
            poke_data = await pokedex_helper.get_poke_by_id(poke)
        except:
            reply = await general_helper.get_info_embd("Pokemon not found", f"Dex entry for id : `{poke}` was not found in the pokedex.\n Most uncommon ids follow this format : \n```{ctx.prefix}dex marowak-alola\n{ctx.prefix}dex gallade-mega\n{ctx.prefix}dex meowstic-female\n{ctx.prefix}dex deoxys-defense\n{ctx.prefix}dex necrozma-dawn\n{ctx.prefix}dex calyrex-shadow-rider\n{ctx.prefix}dex cinderace-gmax```\nIf you still think this pokemon is missing, report it at official server", ERROR_COLOR)
            view = GeneralView(200)

            await ctx.send(embed=reply, view=view)
            return

        reply = await pokedex_helper.get_dex_entry_embed(poke_data)

        view = View()
        view.add_item(Button(label="Comp. Guide", url=POKEMON_LINK_TEMPLATE_SMOGON.format(pokemon=poke), style=ButtonStyle.link))
        view.add_item(Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link))

        await ctx.send(embed=reply, view=view)

    @dex.error
    async def dex_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd(title="Error!!", desc=f"Please provide a `Pokemon_Name` or `Pokemon_ID` as a parameter like```{ctx.prefix}dex minior```", color=ERROR_COLOR)
            await ctx.reply(embed=reply)
        

    """Check Abilities"""
    @commands.command(name="ability", aliases=["ab"], description="Get ability details")
    @commands.guild_only()
    async def ability(self, ctx:commands.Context, name):
        
        reply = await pokedex_helper.get_ability_embed(name)
        view = View()
        
        view.add_item(Button(label="Learn More", url=ABILITY_LINK_TEMPLATE_SMOGON.format(ability=name), style=ButtonStyle.link))
        view.add_item(Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link))

        await ctx.send(embed=reply, view=view)

    @ability.error
    async def ability_handler(self, ctx:commands.Context, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Missing Argument Error!", f"Give an ability as parameter like ```{ctx.prefix}ability stance-change```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)
            
            await ctx.reply(embed=reply, view=view)

def setup(bot):
    bot.add_cog(PokeDex(bot))