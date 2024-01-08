import discord
from discord.ext import commands

from views.ButtonViews import GeneralView
import config


class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx: commands.Context):
        """View all the mails in the mailbox"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        view = GeneralView()

        embd.description = "---------------------_**New**_---------------------\n\n"
        # embd.description += f"# Tierlists \nNew GEN9 ready pokemon tierlists are now available thanks to [falonius]({config.USER_PROFILE_TEMPLATE.format(user_id=450849605358321675)}). \n\nYou think someone is not at their correct place? Lets discuss it at the [official server]({config.SUPPORT_SERVER_LINK})"

        embd.description += "\n\n---------------------_**Old**_---------------------\n\n"
        embd.description += "Its time for a brand new feature coming to aerial ace. Introducing...\n# Donation Logging\n\nDonation Logging is a module ( set of commands ) which automatically logs donation, calculate their approximate worth, create a leaderboard based on the pc value of the donations all while making them easier to track and manage."

        embd.description += "\n\nThanks for using Aerial Ace as always."

        await ctx.send(embed=embd, view=view)


# Mail reminder
async def process_mail(ctx):
    embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
    embd.description = f"** New Updated Tierlists **"
    try:
        embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
    except Exception as e:
        pass  # Don't add footer in mail reminder through slash commands

    await ctx.send(embed=embd)


def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)
