from discord import ApplicationContext
from discord.ext import commands
from discord.commands import slash_command

from views.ButtonViews import GeneralView, DonationView
from helpers import utility_helper

class UtilitySlash(commands.Cog):
    
    """Bot's latency"""

    @slash_command(name="ping", description="Get bot's current latency")
    async def ping(self, ctx):
        ping = str(round(ctx.bot.latency * 1000, 2))
        view = GeneralView(200, True, True, False, True)
        await ctx.respond(f"Pong! Took {ping} ms", view=view)

    """Rolls a dice"""

    @slash_command(name="roll", description="Roll a die with provided upper limit")
    async def roll(self, ctx : ApplicationContext, max : int = 100):
        reply = await utility_helper.roll(max, ctx.author)
        view = GeneralView(200, True, True, False, True)
        await ctx.respond(reply, view=view)

    """Support Server Link"""

    @slash_command(name="support_server", description="Link for joining the support server")
    async def support_server(self, ctx : ApplicationContext):
        reply = await utility_helper.get_support_server_embed()
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """Vote Link"""

    @slash_command(name="vote", description="Link for voting page of the bot")
    async def vote(self, ctx : ApplicationContext):
        reply = await utility_helper.get_vote_embed()
        view = GeneralView(200, True, False, False, True)

        await ctx.respond(embed=reply, view=view)

    """Invite LInk"""

    @slash_command(name="invite", description="Link for inviting the bot")
    async def invite(self, ctx : ApplicationContext):
        reply = await utility_helper.get_invite_embed()
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)
    
    """About the bot"""

    @slash_command(name="about", description="About the bot")
    async def about(self, ctx : ApplicationContext):
        reply = await utility_helper.get_about_embed(ctx)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

    """Donation Links"""

    @slash_command(name="donation", description="Donate or become a patron to support the development of aerial ace")
    async def donation(self, ctx:ApplicationContext):
        reply = await utility_helper.get_donation_embed()
        view = DonationView(200)

        await ctx.respond(embed=reply, view=view)


def setup(bot : commands.Bot):
    bot.add_cog(UtilitySlash())