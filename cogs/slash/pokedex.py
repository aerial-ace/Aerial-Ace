from discord.ext import commands

from discord_slash import SlashContext, SlashCommandOptionType
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option

from cog_helpers import pokedex_helper
from cog_helpers import weakness_helper

class Pokedex_Slash_Module(commands.Cog):
    
    @cog_ext.cog_slash(name="dex", description="Returns the dex entry of the pokemon", options=[
        create_option(name="name_or_id", description="Enter the name of the pokemon", option_type=SlashCommandOptionType.STRING, required=True)
    ])
    async def dex(self, ctx : SlashContext, name_or_id : str):
        data = await pokedex_helper.get_poke_by_id(name_or_id)
        reply = await pokedex_helper.get_dex_entry_embed(data)

        await ctx.send(embed=reply)

    
    @cog_ext.cog_slash(name="ping", description="Get the bot's latency")
    async def ping(self, ctx: SlashContext):
        await ctx.send(str(ctx.bot.latency))

    @cog_ext.cog_slash(name="weak", description="Returns the type weakness of the pokemon", options=[
        create_option(name="pokemon", description="Name of the pokemon", option_type=SlashCommandOptionType.STRING, required=True)
    ])
    async def weakness(self, ctx:SlashContext, pokemon):
        embd = await weakness_helper.get_weakness_embed(ctx, [pokemon])

        await ctx.send(embed=embd)

def setup(bot : commands.Bot):
    bot.add_cog(Pokedex_Slash_Module())