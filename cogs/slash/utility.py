from discord import Embed, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from cog_helpers import utility_helper

class UtilitySlash(commands.Cog):
    
    @slash_command(name="roll", description="Roll a die with provided upper limit", guild_ids=[751076697884852389])
    async def roll(self, ctx : ApplicationContext, max : int = 100):
        reply = await utility_helper.roll(max, ctx.author)
        await ctx.respond(reply)

    @slash_command(name="support_server", description="Link for joining the support server", guild_ids=[751076697884852389])
    async def support_server(self, ctx : ApplicationContext):
        reply = await utility_helper.get_support_server_embed()
        await ctx.respond(embed=reply)

    @slash_command(name="vote", description="Link for voting page of the bot", guild_ids=[751076697884852389])
    async def vote(self, ctx : ApplicationContext):
        reply = await utility_helper.get_vote_embed()
        await ctx.respond(embed=reply)

    @slash_command(name="invite", description="Link for inviting the bot", guild_ids=[751076697884852389])
    async def invite(self, ctx : ApplicationContext):
        reply = await utility_helper.get_invite_embed()
        await ctx.respond(embed=reply)
    
    @slash_command(name="about", description="About the bot", guild_ids=[751076697884852389])
    async def about(self, ctx : ApplicationContext):
        reply = await utility_helper.get_about_embed(ctx)
        await ctx.respond(embed=reply)

def setup(bot : commands.Bot):
    bot.add_cog(UtilitySlash())