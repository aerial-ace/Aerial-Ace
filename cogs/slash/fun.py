from discord import Member, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import fun_helper
from views.ButtonViews import GeneralView

class FunSystemSlash(commands.Cog):
    
    """Kill someone"""

    @slash_command(name="kill", description="Kill someone, the pokemon way")
    async def kill(self, ctx : ApplicationContext, target : Option(Member, description="Member to kill", required=True)):

        if target == ctx.author : 
            await ctx.respond("I was unable to find a suicide gif, but dw, you **successfully** killed yourself :]")
            return

        reply = await fun_helper.get_kill_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

    """Hit someone"""

    @slash_command(name="hit", description="Hit someone, the pokemon way")
    async def hit(self, ctx : ApplicationContext, target : Option(Member, description="Member to hit", required=True)):

        reply = await fun_helper.get_hit_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)
       
    """Dance with/without someone"""

    @slash_command(name="dance", description="Dance Dance, the pokemon way")
    async def dance(self, ctx : ApplicationContext, target : Option(Member, description="Member to dance with", required=False, default=None)):

        if target is None:
            embd = await fun_helper.get_dance_embed(ctx.author)
        else:
            embd = await fun_helper.get_dance_embed(ctx.author, target)

        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=embd, view=view)

    """Pat someone"""

    @slash_command(name="pat", description="Pat Pat, the pokemon way")
    async def pat(self, ctx : ApplicationContext, target : Option(Member, description="Member to pat", required=True)):

        reply = await fun_helper.get_pat_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

    """Tease someone"""

    @slash_command(name="tease", description="Tease someone, cz why not")
    async def tease(self, ctx : ApplicationContext, target : Option(Member, description="Member to tease", required=True)):

        reply = await fun_helper.get_tease_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

    """Cry using gifs"""

    @slash_command(name="cry", description="Cry, the pokemon way")
    async def cry(self, ctx:ApplicationContext):

        reply = await fun_helper.get_cry_embed(ctx.author)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

    """Hug using Gifs"""

    @slash_command(name="hug", description="Hug someone, the pokemon way")
    async def hug(self, ctx:ApplicationContext, target:Option(Member, description="Member to hug", required=True)):

        reply = await fun_helper.get_hug_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, False)

        await ctx.respond(embed=reply, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(FunSystemSlash())