import discord
from discord.ext import commands
from discord.commands import slash_command
from discord.commands import Option

from cog_helpers import pokedex_helper

class PokedexSlash(commands.Cog):

    """Bot's latency"""

    @slash_command(name="ping", guild_ids=[751076697884852389])
    async def ping(self, ctx):
        ping = str(round(ctx.bot.latency * 1000, 2))
        await ctx.respond(f"Pong! Took {ping} ms")

    """Dex entry of the pokemon"""

    @slash_command(name="dex", description="Shows the dex entry of the pokemon", guild_ids=[751076697884852389])
    async def dex(self, ctx, pokemon : Option(str)):
        poke = await pokedex_helper.get_poke_by_id(pokemon)
        reply = await pokedex_helper.get_dex_entry_embed(poke)

        await ctx.respond(embed=reply)

    """Random Pokemon Slash Command"""

    @slash_command(name="random_pokemon", description="Shows a randomly choosen pokemon", guild_ids=[751076697884852389])
    async def random_pokemon(self, ctx):
        poke = await pokedex_helper.get_random_poke()
        reply = await pokedex_helper.get_random_pokemon_embed(poke)

        await ctx.respond(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(PokedexSlash())