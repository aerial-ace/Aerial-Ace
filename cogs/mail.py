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

        embd.description += f"All premium servers will now receive Streak Detection System to log your 100th, 1000th, 10000th, 100000th, 1000000th, 10...(etc) catches to starboard. \nComes with all new look and feel. \nDonate to support the development and get this feature ( with many others ) right now\n\n"

        embd.description += ">>>>>>>__**Old**__\n\n"
        embd.description += "Aerial Ace has introduced **Starboard Customization Module** for its supporters! You now get a set of various commands to customize the starboard of your server to whatever way you like [ LITERALLY ]. The extent  is broken down into various tiers, each enabling different level of customization. Tiers are listed below : \n\n"

        embd.description += f"{config.BULLET_EMOJI} **TIER-3 : **\n"
        embd.description += "Fully customizable starboard text! \n_You can now update the text of rare catch embed, and say a lot of things whether it be something more than Congrats, or straight out ask for its stats._\n\n"

        embd.description += f"{config.BULLET_EMOJI} **TIER-2 : **\n"
        embd.description += "Fully customizable starboard image. \n_Server of this tier will get access to custom starboard rare/shiny catch image. Update it to your server mascot or pick a good anime gif, and slap it in, the choice is yours._\n"
        embd.description += "Include rewards from the previous tiers.\n\n"

        embd.description += f"{config.BULLET_EMOJI} **TIER-1 : **\n"
        embd.description += "Fully [ We mean FULLY ] customizable starboard embed. \n_Servers of this tier have full control over how the starboard embed should look like. You can add custom invite links, vote links, messages, ask the users to perform certain task on catching a rare/shiny [ Good for events ] and what not. Definitely the most powerful and good for servers with a lot of events happening._\n"
        embd.description += "Includes rewards from the previous tiers\n\n"

        embd.description += "**To check the pricing, visit our patreon page.**\n\n"

        embd.description += "__By becoming a member of these tiers, you directly support the development of Aerial Ace. The base functionality of aerial-ace is and will always be 100% free. These customizations are just a way to thank our awesome supporters who keep the bot alive.__"
        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = 75
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Introducing, Streak Catch Detection. Available to all tiers!"
            try:
                embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
            except:
                pass # Dont add footer in mail reminder through slash commands

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)