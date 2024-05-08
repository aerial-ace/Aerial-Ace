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
        embd.description += f"**Starboard Update** : Premium Servers now log rare low ( < 5% ) and high ( > 95% ) iv pokemons in the starboard. This option is enabled by default. Enjoy!"
        embd.description += "\n\n"

        embd.description += "```Old```\n"
        embd.description += f"Introducing Spawn Speed Module! Using this module, you can assign a Voice/Stage Channel and it will show the number of spawns per hour in your server. Get started with `-aa help spawnrate`"

        embd.description += "\n\nThanks for using Aerial Ace as always."

        embd.set_image(url="https://cdn.discordapp.com/attachments/908392246158700607/1204798879816613950/image.png?ex=65d60b65&is=65c39665&hm=89bdb9952f01bdd1ce032f3919b88c249183d613235a4323bff96ecfaa39587d")

        await ctx.send(embed=embd, view=view)   


# Mail reminder
async def process_mail(ctx):
    embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
    embd.description = f"** Low/High IV Starboard **"
    try:
        embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
    except Exception as e:
        pass  # Don't add footer in mail reminder through slash commands

    await ctx.send(embed=embd)


def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)
