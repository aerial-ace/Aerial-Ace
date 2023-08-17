import discord
from discord.ext import commands

from views.ButtonViews import DonationView
import config

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        view = DonationView(2000)
        
        embd.description = ">>>>>>>__**New**__\n\n"
        embd.description += f"All the Scarlet/Violet Pokemon Movesets are now added! "

        embd.description += "\n\n>>>>>>>__**Old**__\n\n"
        embd.description += f"Introducing the all-new Random Ruleset feature of Aerial Ace. Are you bored of doing your usual battles? Are in for some fun battle experience? Run the command `-aa random_ruleset` to fetch random rules for your next battle. Enforce these rules on your battles to make them fun and challenging. There are many rules added, and you can contribute your own rulesets too. Hope on our Support Server and suggest your own cool ruleset for everyone to try. Good luck on your next rando battles."

        embd.description += "\n\nThanks for using Aerial Ace as always."

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
        embd.description = f"**Scarlet/Violet** pokemon movesets are here!"
        try:
            embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
        except:
            pass # Dont add footer in mail reminder through slash commands

        await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)