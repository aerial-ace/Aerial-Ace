import discord
from discord.ext import commands
import random

import config

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"])
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        embd.description = f"{config.IMPORTANT_EMOJI} For Admins {config.IMPORTANT_EMOJI}\n"

        embd.description += f"Aerial Ace now supports **Slash Commands**. To get them working though, you need to reauthorize the bot for your server. \n\n"
        embd.description += f"Just click on the [invite link]({config.INVITE_LINK}), select your server and click authorize\n\n"

        embd.description += f"To get started, use `/dance` {config.THEFK_EMOJI}"

        await ctx.send(embed=embd)

# Mail reminder
async def process_mail(ctx):

        prob : int = 50
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} Mail Box {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Very Important Mail is in the mail box\n"
            embd.description += f"Check using `{ctx.prefix}mail` now"
            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)