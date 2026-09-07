from discord import ApplicationContext
from discord.commands import slash_command
from discord.ext import commands

from helpers import mail_helper
from views.ButtonViews import GeneralView


class MailModuleSlash(commands.Cog):
    @slash_command(name="help", description="Get help for a command", guild_ids=[751076697884852389])
    async def help(self, ctx: ApplicationContext):

        embd = await mail_helper.get_mail_embed()
        view = GeneralView(200, True, True, True, True)

        await ctx.respond(embed=embd, view=view)


def setup(bot: commands.Bot):
    bot.add_cog(MailModuleSlash())
