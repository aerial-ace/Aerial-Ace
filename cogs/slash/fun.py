from discord import Member, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import fun_helper

class FunSystemSlash(commands.Cog):
    
    """Kill someone"""

    @slash_command(name="kill", description="Kill someone, the pokemon way", guild_ids=[751076697884852389])
    async def kill(self, ctx : ApplicationContext, target : Option(Member, description="Member to kill", required=True)):

        if target == ctx.author : 
            await ctx.respond("I was unable to find a suicide gif, but dw, you **successfully** killed yourself :]")
            return

        reply = await fun_helper.get_kill_embed(ctx.author, target)
        await ctx.respond(embed=reply)

    """Hit someone"""

    @slash_command(name="hit", description="Hit someone, the pokemon way", guild_ids=[751076697884852389])
    async def hit(self, ctx : ApplicationContext, target : Option(Member, description="Member to hit", required=True)):

        reply = await fun_helper.get_hit_embed(ctx.author, target)

        await ctx.respond(embed=reply)
       
    """Dance with/without someone"""

    @slash_command(name="dance", description="Dance Dance, the pokemon way", guilds_ids=[751076697884852389])
    async def dance(self, ctx : ApplicationContext, target : Option(Member, description="Member to dance with", required=False, default=None)):

        if target is None:
            embd = await fun_helper.get_dance_embed(ctx.author)
        else:
            embd = await fun_helper.get_dance_embed(ctx.author, target)

        await ctx.respond(embed=embd)

    """Pat someone"""

    @slash_command(name="pat", description="Pat Pat, the pokemon way", guild_ids=[751076697884852389])
    async def pat(self, ctx : ApplicationContext, target : Option(Member, description="Member to pat", required=True)):

        reply = await fun_helper.get_pat_embed(ctx.author, target)

        await ctx.respond(embed=reply)

    """Tease someone"""

    @slash_command(name="tease", description="Tease someone, cz why not", guild_ids=[751076697884852389])
    async def tease(self, ctx : ApplicationContext, target : Option(Member, description="Member to tease", required=True)):

        reply = await fun_helper.get_tease_embed(ctx.author, target)

        await ctx.respond(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(FunSystemSlash())