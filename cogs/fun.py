from click import command
import discord
from discord.ext import commands

from cog_helpers import general_helper
from cog_helpers import fun_helper
import config

class FunModule(commands.Cog):

    @commands.guild_only()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="kill")
    async def kill(self, ctx, target : discord.Member):

        """Kill someone by showing gifs"""

        if target == ctx.author : 
            await ctx.reply("I was unable to find a suicide gif, but dw, you **successfully** killed yourself :]")
            return

        reply = await fun_helper.get_kill_embed(ctx.author.name, target.name)

        await ctx.send(embed=reply)
        
    @kill.error
    async def kill_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}kill @Pumpkaboo```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

    @commands.guild_only()
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    @commands.command(name="hit")
    async def hit(self, ctx, target : discord.Member):

        """Hit someone by showing gifs"""

        if ctx.author == target:
            reply = discord.Embed(title=f"{ctx.author.name} slapped {ctx.author.name} then, {ctx.author.name} slapped {ctx.author.name} :/ What a mess.").set_image(url="https://cdn.discordapp.com/attachments/893732055421157396/934808056343191552/psyduck-hit-smash.gif")
            await ctx.send(embed=reply)
            return

        reply = await fun_helper.get_hit_embed(ctx.author.name, target.name)
        await ctx.send(embed=reply)

    @hit.error
    async def hit_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}hit @Irrbis```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="dance")
    async def dance(self, ctx, target : discord.Member = None):
        if target is None:
            reply = await fun_helper.get_dance_embed(ctx.author.name)
        else:
            reply = await fun_helper.get_dance_embed(ctx.author.name, target.name)

        await ctx.send(embed=reply)

    @dance.error
    async def dance_handler(self, ctx, error):
        await ctx.reply(error)

    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(name="pat")
    async def pat(self, ctx, target : discord.Member):
        reply = await fun_helper.get_pat_embed(ctx.author.name, target.name)
        await ctx.send(embed=reply)

    @pat.error
    async def pat_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}pat @raupy```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

    @commands.guild_only()
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command(name="tease")
    async def tease(self, ctx, target : discord.Member):
        reply = await fun_helper.get_tease_embed(ctx.author.name, target.name)
        await ctx.send(embed=reply)

    @pat.error
    async def tease_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingPermissions):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}pat @raupy```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

def setup(bot):
    bot.add_cog(FunModule())