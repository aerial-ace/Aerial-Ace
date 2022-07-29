from discord import ApplicationContext, AutocompleteContext
from discord.ext import commands
from discord.commands import slash_command, Option

from views.ButtonViews import GeneralView
from cog_helpers import pokemon_info_helper
import config

class PokeInfoSlash(commands.Cog):

    """For getting best duel stats"""

    @slash_command(name="stats", description="Returns the best duel stats of the pokemon")
    async def stats(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_stats_embed(pokemon)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """For getting best duel moveset"""

    @slash_command(name="moveset", description="Returns the best moveset of the pokemon")
    async def moveset(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_moveset_embed(pokemon)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """For getting the best duel nature"""

    @slash_command(name="nature", description="Returns the best nature for the pokemon")
    async def nature(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_nature_embed(pokemon)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """For getting the weakness"""

    @slash_command(name="weak", description="Returns the type weaknesses of the pokemon")
    async def weakness(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_weakness_embed([pokemon])
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)


    """For getting tierlists"""

    tierlist_catagories = ["common", "mega", "rare", "bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water", "eeveelution"]

    # return catagory from the input
    async def get_catagory(self, ctx : AutocompleteContext) -> str:
        return [catagory for catagory in self.tierlist_catagories if catagory.startswith(ctx.value)]

    @slash_command(name="tierlist", description="Returns the tier list of the select catagory")
    async def tierlist(self, ctx : ApplicationContext, catagory : Option(str, description="Select Catagory", required=True, autocomplete=get_catagory)):

        tier_link = config.TIER_LINK[catagory]
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(tier_link, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(PokeInfoSlash())