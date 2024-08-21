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

        embd.description = "```New```\n"
        embd.description += f"PREMIUM FEATURE! Alert Disabling. You can now customize which alerts are shown before logging the catches. If disabled, no alert of that type will be shown but the catch will be logged in the starboard.\n\n To know more, `aa.help starboard`"
        embd.description += "\n\n"

        embd.description += "```Old```\n"
        embd.description += f"Separate Logging Channels for Rare and Shiny Pokemons. You can now set a different channel for shiny starboard logs which will allows server owners to showcase the shiny catches in their server in different channels. These channels will only be used for shiny catches and other catches like rare / regional and catch streaks will all be sent to default logging channel like usual. To enable this in your server, use the command `aa.sb shch <shiny_channel>`. For more info, visit the Support Server. \n\n ** ALSO, Low and High IV logs are now open for all servers ( both premium and free servers ). We hope you like this new addition. If you have any suggestions, please let us know. **"

        embd.description += "\n\nThanks for using Aerial Ace as always."

        await ctx.send(embed=embd, view=view)   


# Mail reminder
async def process_mail(ctx):
    embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
    embd.description = f"** Premium Feature : Alert Disabling **"
    try:
        embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
    except Exception as e:
        pass  # Don't add footer in mail reminder through slash commands

    await ctx.send(embed=embd)


def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)
