from discord import ApplicationContext, AutocompleteContext
from discord.ext import commands
from discord.commands import slash_command, Option

import config
from cog_helpers import pokemon_info_helper

class PokeInfoSlash(commands.Cog):

    """For getting best duel stats"""

    @slash_command(name="stats", description="Returns the best duel stats of the pokemon", guild_ids=[751076697884852389])
    async def stats(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_stats_embed(pokemon)

        await ctx.respond(embed=reply)

    """For getting best duel moveset"""

    @slash_command(name="moveset", description="Returns the best moveset of the pokemon", guild_ids=[751076697884852389])
    async def moveset(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_moveset_embed(pokemon)

        await ctx.respond(embed=reply)

    """For getting the best duel nature"""

    @slash_command(name="nature", description="Returns the best nature for the pokemon", guild_ids=[751076697884852389])
    async def nature(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_nature_embed(pokemon)

        await ctx.respond(embed=reply)

    """For getting the weakness"""

    @slash_command(name="weak", description="Returns the type weaknesses of the pokemon", guild_ids=[751076697884852389])
    async def weakness(self, ctx : ApplicationContext, pokemon : Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_weakness_embed([pokemon])

        await ctx.respond(embed=reply)


    """For getting tierlists"""

    tierlist_catagories = ["common", "mega", "rare", "bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

    # return catagory from the input
    async def get_catagory(self, ctx : AutocompleteContext) -> str:
        return [catagory for catagory in self.tierlist_catagories if catagory.startswith(ctx.value)]

    @slash_command(name="tierlist", description="Returns the tier list of the select catagory", guild_ids=[751076697884852389])
    async def tierlist(self, ctx : ApplicationContext, catagory : Option(str, description="Select Catagory", required=True, autocomplete=get_catagory)):

        tier_link = config.TIER_LINK[catagory]

        await ctx.respond(tier_link)

def setup(bot : commands.Bot):
    bot.add_cog(PokeInfoSlash())