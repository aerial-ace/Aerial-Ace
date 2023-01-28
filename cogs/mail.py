import discord
from discord.ext import commands
import random

from views.ButtonViews import GeneralView, DonationView
import config

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        view = DonationView(2000)
        
        embd.description = ">>>>>>>__**New**__\n\n"
        embd.description += f"All servers will now receive access to Auto Battle Logging Module. This module ( if turned on ) will automatically log battle results to the server battle board. \nUse `-aa abl` to toggle this module. \nUse `-aa blb` to check this server's battle board. \nUse `-aa help battle` for help in battle related commands."

        embd.description += "\n\n>>>>>>>__**Old**__\n\n"
        embd.description += f"All premium servers will now receive Streak Detection System to log your 100th, 1000th, 10000th, 100000th, 1000000th, 10...(etc) catches to starboard. \nComes with all new look and feel. \nDonate to support the development and get this feature ( with many others ) right now\n\n"

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = 50
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Introducing **Automatic Battle Logging!** Out now in all servers."
            try:
                embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
            except:
                pass # Dont add footer in mail reminder through slash commands

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)