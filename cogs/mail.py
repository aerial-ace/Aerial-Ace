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
        embd.description = f"{config.IMPORTANT_EMOJI} For Admins {config.IMPORTANT_EMOJI}\n\n"

        embd.description += f"Aerial Ace now has a Starboard System. Use `{ctx.prefix}starboard #channel` to enable it.\n\n"
        embd.description += f"Here is how the embeds look {config.THEFK_EMOJI}"
        embd.set_image(url="https://cdn.discordapp.com/attachments/908392246158700607/944602162900635658/unknown.png")

        await ctx.send(embed=embd)

# Mail reminder
async def process_mail(ctx):

        prob : int = 20
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} Mail Box {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Starboard System is here :tada:\n\n"
            embd.description += f"Check using `{ctx.prefix}mail` now"
            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)