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
        embd.description += f"After **A VERY LONG** time, we finally have Galar Pokemon Moves in Poketwo. We are working towards including all the required battle data for these galar pokemon, so that you can build your best teams and hopefully survive the new meta that is going to develop around these galar pokemons. \nWe have already included **Galar Stats**, and you can check those using `-aa stats <pokemon>` command. \n\n**NOTE** : Galar Pokemons are a very new introduction to the previous battle system, so it will take time until we all figure out which stats are best for which pokemon. So take these stats with a grain of salt, We do encourage players to try out different sets and help us make our stats database robust and error proof. \n\nThanks for using Aerial Ace as always <3"

        embd.description += "\n\n>>>>>>>__**Old**__\n\n"
        embd.description += f"All servers will now receive access to Auto Battle Logging Module. This module ( if turned on ) will automatically log battle results to the server battle board. \nUse `-aa abl` to toggle this module. \nUse `-aa blb` to check this server's battle board. \nUse `-aa help battle` for help in battle related commands."

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = 50
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Introducing **Galar Stats** data in aerial ace."
            try:
                embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
            except:
                pass # Dont add footer in mail reminder through slash commands

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)