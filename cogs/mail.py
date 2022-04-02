import discord
from discord.ext import commands
import random

import config
from views.GeneralView import GeneralView

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"], description="open the mail box to get alerts")
    async def open_mail(self, ctx : commands.Context):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        view = GeneralView(200, True, True, False, False)
        
        embd.description = "__**New**__\n\n"

        embd.description += f"{config.BULLET_EMOJI}Movesets/Stats/Nature data for alolan pokemons is now available.\n"

        embd.description += "\n__**Older**__\n\n"
        embd.description += f"{config.BULLET_EMOJI}Admins are requested to reathorize the bot by click on the [invite link]({config.INVITE_LINK}) and then click on reauthorize after selecting the server. Its required to use slash commands in your server.\n"
        embd.description += f"{config.BULLET_EMOJI}Rerun the starboard command if you are/want to use built-in powerfull starboard system.\n"

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = 15
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} Mail Box {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Alolan Pokemons are here"
            embd.set_footer(text=f"Check using {ctx.prefix}mail")

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)