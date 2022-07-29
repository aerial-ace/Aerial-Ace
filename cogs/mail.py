import discord
from discord.ext import commands
import random

from views.ButtonViews import GeneralView
import config

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        view = GeneralView(200, True, True, False, True)
        
        embd.description = "__**New**__\n\n"

        embd.description += f"{config.BULLET_EMOJI}Eeveelution Tier List added [Beta]. Try `{ctx.prefix}tl eeveelution` \n"
        embd.description += f"{config.BULLET_EMOJI}New Smogon Commands is now available. Use this `smogon` command to get the usage statistics of any pokemon. Try `{ctx.prefix}smogon 8 OU dragapult`. \n"
        embd.description += f"{config.BULLET_EMOJI}Suggest command is here, use `{ctx.prefix}suggest` command to send a suggestion to the developers.\n"

        embd.description += "\n__**Older**__\n\n"
        embd.description += f"{config.BULLET_EMOJI}Movesets/Stats/Nature data for alolan pokemons is now available.\n"
        embd.description += f"{config.BULLET_EMOJI}Admins are requested to reathorize the bot by click on the [invite link]({config.INVITE_LINK}) and then click on reauthorize after selecting the server. Its required to use slash commands in your server.\n"

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = -1
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} Mail Box {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Smogon | Suggest commands are here"
            embd.set_footer(text=f"Check using {ctx.prefix}mail")

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)