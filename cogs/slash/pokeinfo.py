from discord import ApplicationContext, AutocompleteContext
from discord.commands import Option, slash_command
from discord.ext import commands

import config
from helpers import pokemon_info_helper
from views.ButtonViews import GeneralView


class PokeInfoSlash(commands.Cog):
    @commands.Cog.listener()
    async def on_ready(self):
        self.default_view = GeneralView(200, True, False, False, True)

    """For getting best duel stats"""

    @slash_command(name="stats", description="Returns the best duel stats of the pokemon")
    async def stats(self, ctx: ApplicationContext, pokemon: Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_stats_embed(pokemon)

        await ctx.respond(embed=reply, view=self.default_view)

    """For getting best duel moveset"""

    @slash_command(name="moveset", description="Returns the best moveset of the pokemon")
    async def moveset(self, ctx: ApplicationContext, pokemon: Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_moveset_embed(pokemon)

        await ctx.respond(embed=reply, view=self.default_view)

    """For getting the best duel nature"""

    @slash_command(name="nature", description="Returns the best nature for the pokemon")
    async def nature(self, ctx: ApplicationContext, pokemon: Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_nature_embed(pokemon)

        await ctx.respond(embed=reply, view=self.default_view)

    """For getting the weakness"""

    @slash_command(name="weak", description="Returns the type weaknesses of the pokemon")
    async def weakness(self, ctx: ApplicationContext, pokemon: Option(str, description="Name of the pokemon", required=True)):

        reply = await pokemon_info_helper.get_weakness_embed([pokemon])

        await ctx.respond(embed=reply, view=self.default_view)

    """For getting tierlists"""

    tierlist_categories: list = ["common", "mega", "rare", "bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water", "eeveelution"]

    # return category from the input
    async def get_category(self, ctx: AutocompleteContext):
        return [category for category in self.tierlist_categories if category.startswith(ctx.value)]

    @slash_command(name="tierlist", description="Returns the tier list of the select category")
    async def tierlist(self, ctx: ApplicationContext, category: Option(str, description="Select category", required=True, autocomplete=get_category)):

        try:
            tier_link = config.TIER_LINK[category.lower()]
        except KeyError:
            return await ctx.respond("That is not a tier. Enter a good tier like `rare`, `mega`, `common`, `steel`, `eeveelution`")

        await ctx.respond(f"{tier_link} - These lists might be outdated! If you can help with updating these, please reach out in the support sever!", view=self.default_view)


def setup(bot: commands.Bot):
    bot.add_cog(PokeInfoSlash())
