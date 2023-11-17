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

        embd.description = "----------------------------------_**New**_----------------------------------\n"
        embd.description += "## Aerial Ace's 2nd Anniversary \nTo celebrate Aerial Ace's 2nd Anniversary, we are giving away Aerial Ace Premium Features! Join the support server to participate. \n\nAnd thanks for your support as always <3"

        embd.description += "\n\n----------------------------------_**Old**_----------------------------------\n\n"
        embd.description += "Its time for a brand new feature coming to aerial ace. Introducing...\n# Donation Logging\n\nDonation Logging is a module ( set of commands ) which automatically logs donation, calculate their approximate worth, create a leaderboard based on the pc value of the donations all while making them easier to track and manage. Owner can allow their admins to collect donation when they are afk, and when they are online, they can collect the same donations from the admins and mark the donation as collected. \n\nIt is a very intuitive feature and will make donation management of your server a breeze. \n\nIt is already implemented in the support server and will soon be implement in some other aerial ace partner servers as well. If you want to look at how it works, head on over to [donation-logging-module-guide](https://discord.com/channels/751076697884852389/1141829994688041092) _(link to the support server)_. \n\nIt is a free to use feature with additional features for all tiers above the first tier! \n\nIts still an early release, so any bug reports, feedbacks, suggestions are highly appreciated."

        embd.description += "\n\nThanks for using Aerial Ace as always."

        await ctx.send(embed=embd, view=view)


# Mail reminder
async def process_mail(ctx):
    embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
    embd.description = f"** :tada: 2nd Anniversary Giveaway :tada: **"
    try:
        embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
    except Exception as e:
        pass  # Don't add footer in mail reminder through slash commands

    await ctx.send(embed=embd)


def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)
