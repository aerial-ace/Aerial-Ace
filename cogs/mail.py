import discord
from discord.ext import commands
import random

import config
from views.GeneralView import GeneralView

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"])
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        embd.description = f"{config.IMPORTANT_EMOJI} For Admins {config.IMPORTANT_EMOJI}\n\n"

        embd.description += f"Random Team Commands are here :tada:\nCheck using `-aa help random_misc`\n\n"
        embd.description += f"{config.ALERT_EMOJI} Admins are requested to rerun the starboard command if they are using it {config.THEFK_EMOJI}"

        await ctx.send(embed=embd)

# Mail reminder
async def process_mail(ctx):

        prob : int = -1
        roll = random.randint(0, 100)

        view = GeneralView(200, True, True, False, False)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} Mail Box {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"{config.ALERT_EMOJI}Admins are requested to rerun the starboard command\n\n"
            embd.description += f"Check using `{ctx.prefix}mail` now"

            await ctx.send(embed=embd, view=view)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)