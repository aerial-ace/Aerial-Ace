import discord
from discord.ext import commands

from views.ButtonViews import GeneralView
from helpers import general_helper
from helpers import fun_helper
import config


class FunModule(commands.Cog):
    """Kill someone by showing gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="kill", description="Kill someone using pokemon gifs")
    async def kill(self, ctx, target: discord.Member):

        if target == ctx.author:
            await ctx.reply("I was unable to find a suicide gif, but dw, you **successfully** killed yourself :]")
            return

        reply = await fun_helper.get_kill_embed(ctx.author, target)

        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @kill.error
    async def kill_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}kill @Pumpkaboo```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)

    """Hit someone by showing gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="hit", description="Hit someone using pokemon gifs")
    async def hit(self, ctx, target: discord.Member):

        reply = await fun_helper.get_hit_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @hit.error
    async def hit_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}hit @Irrbis```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)

    """Dance with someone using gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dance", description="Dance solo, or with someone using pokemon gifs")
    async def dance(self, ctx, target: discord.Member = None):
        if target is None:
            reply = await fun_helper.get_dance_embed(ctx.author)
        else:
            reply = await fun_helper.get_dance_embed(ctx.author, target)

        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @dance.error
    async def dance_handler(self, ctx, error):
        await ctx.reply(error)

    """Pat someone with gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pat", description="Pat someone using pokemon gifs")
    async def pat(self, ctx, target: discord.Member):
        reply = await fun_helper.get_pat_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @pat.error
    async def pat_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}pat @raupy```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)

    """Tease someone with gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name="tease", description="Tease someone using pokemon gifs")
    async def tease(self, ctx, target: discord.Member):
        reply = await fun_helper.get_tease_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @pat.error
    async def tease_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}pat @raupy```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)

    """Cry with gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="cry", description="Cry using pokemon gifs")
    async def cry(self, ctx: commands.Context):
        reply = await fun_helper.get_cry_embed(ctx.author)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @cry.error
    async def cry_handler(self, ctx: commands.Context, error):
        await ctx.reply(error)

    """Hug with gifs"""

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="hug", description="Hug someone using pokemon gifs")
    async def hug(self, ctx: commands.Context, target: discord.Member):
        reply = await fun_helper.get_hug_embed(ctx.author, target)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @cry.error
    async def hug_handler(self, ctx: commands.Context, error):
        await ctx.reply(error)


def setup(bot):
    bot.add_cog(FunModule())
