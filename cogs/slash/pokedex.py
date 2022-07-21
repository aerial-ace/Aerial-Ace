from discord.ext import commands
from discord import ApplicationContext, ButtonStyle
from discord.ui import View, Button
from discord.commands import slash_command
from discord.commands import Option

from cog_helpers import pokedex_helper
from config import ABILITY_LINK_TEMPLATE_SMOGON, POKEMON_LINK_TEMPLATE_SMOGON, INVITE_LINK

class PokedexSlash(commands.Cog):

    """Dex entry of the pokemon"""

    @slash_command(name="dex", description="Shows the dex entry of the pokemon")
    async def dex(self, ctx, pokemon : Option(str)):
        poke = await pokedex_helper.get_poke_by_id(pokemon)
        reply = await pokedex_helper.get_dex_entry_embed(poke)

        view = View()
        view.add_item(Button(label="Comp. Guide", url=POKEMON_LINK_TEMPLATE_SMOGON.format(pokemon=pokemon), style=ButtonStyle.link))
        view.add_item(Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link))

        await ctx.respond(embed=reply, view=view)

    """Get info about abilities"""

    @slash_command(name="ability", description="Details about abilities")
    async def ability(self, ctx:ApplicationContext, name:Option(str, description="Name of the ability", required=True)):
        reply = await pokedex_helper.get_ability_embed(name)
        
        view = View()
        view.add_item(Button(label="Learn More", url=ABILITY_LINK_TEMPLATE_SMOGON.format(ability=name), style=ButtonStyle.link))
        view.add_item(Button(label="Invite", url=INVITE_LINK, style=ButtonStyle.link))

        await ctx.respond(embed=reply, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(PokedexSlash())