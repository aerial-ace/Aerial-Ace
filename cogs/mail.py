from discord.ext import commands

from helpers import mail_helper
from views.ButtonViews import GeneralView


class MailModule(commands.Cog):
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx: commands.Context):
        """View all the mails in the mailbox"""

        embd = await mail_helper.get_mail_embed()
        view = GeneralView()

        await ctx.send(embed=embd, view=view)


# Mail reminder
async def process_mail(ctx):
    await ctx.send(":envelope: MAIL: ** Premium Feature : Alert Disabling **")


def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)
