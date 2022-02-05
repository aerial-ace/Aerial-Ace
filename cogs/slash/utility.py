from discord import Embed, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import utility_helper

class UtilitySlash(commands.Cog):
    
    """Bot's latency"""

    @slash_command(name="ping")
    async def ping(self, ctx):
        ping = str(round(ctx.bot.latency * 1000, 2))
        await ctx.respond(f"Pong! Took {ping} ms")

    """Rolls a dice"""

    @slash_command(name="roll", description="Roll a die with provided upper limit")
    async def roll(self, ctx : ApplicationContext, max : int = 100):
        reply = await utility_helper.roll(max, ctx.author)
        await ctx.respond(reply)

    """Support Server Link"""

    @slash_command(name="support_server", description="Link for joining the support server")
    async def support_server(self, ctx : ApplicationContext):
        reply = await utility_helper.get_support_server_embed()
        await ctx.respond(embed=reply)

    """Vote Link"""

    @slash_command(name="vote", description="Link for voting page of the bot")
    async def vote(self, ctx : ApplicationContext):
        reply = await utility_helper.get_vote_embed()
        await ctx.respond(embed=reply)

    """Invite LInk"""

    @slash_command(name="invite", description="Link for inviting the bot")
    async def invite(self, ctx : ApplicationContext):
        reply = await utility_helper.get_invite_embed()
        await ctx.respond(embed=reply)
    
    """About the bot"""

    @slash_command(name="about", description="About the bot")
    async def about(self, ctx : ApplicationContext):
        reply = await utility_helper.get_about_embed(ctx)
        await ctx.respond(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(UtilitySlash())