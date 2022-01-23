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

        reply = await fun_helper.get_hit_embed(ctx.author.name, target.name)
        await ctx.send(embed=reply)

    @hit.error
    async def hit_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this : ```{ctx.prefix}hit @Irrbis```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.reply(error)

def setup(bot):
    bot.add_cog(FunModule())