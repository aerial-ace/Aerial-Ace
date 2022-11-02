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

        embd.description += f"After being in service for about a year now. We are finally going to be taking aerial ace down from 25th November 2022. The reason mainly being the funding. Aerial Ace was always supposed to be 100% free to use and OPEN SOURCE. All features and commands were provided free of cost to anyone and everyone. Though this was all good for a small bot in a few servers but not for a bot of current scale in which aerial ace is. The cost of managing the servers and database for current user base is not easy (and not cheap). We ( one man team ) work on aerial ace without any income of any sort because we enjoy making stuff that people use. But considering the scale of aerial ace, it is getting harder and harder to manage the costs on our side. We already work on aerial ace and provide updates just so that the community can get benefited from them whether it is collecting battle data of LITERALLY hundreds of pokemon one by one (it was a pain yes) or creating a rare catch detection system that is unrivaled by any bot at the moment. It takes time and efforts to bring these changes to life and we are ready to put those efforts. But as we said earlier, making the best poketwo helper bot is not our issue, keeping the bot alive is. Due to this reason, We have decided to discontinue Aerial Ace. All the other stuff, including the github repository and the support server will remain active for those who want to ask stuff in the aerial ace repo or just want to be a member of the bot's community that they like. \n\nIt is not the end though, you can still keep aerial ace alive by either donating or becoming a patron ( links in the buttons ). Even your smallest donations can help aerial ace be the best it is. Of course, none of your donation are going to be used for a secret chill party or anything, all the funds will be used directly to sustain aerial ace and make improvements [ You can become a patron, so that your changes are brought to life the earliest ]. Donation and Patron links are provided in the buttons [ Let me know if any of them is not working ]. If you are a techy person, you can also sponsor the repo on github. We give cool rewards there as well :]\n\n**TLDR:** \n{config.BULLET_EMOJI}Aerial Ace is going to be discontinued from 25th November 2022\n{config.BULLET_EMOJI}At the current scale, it is getting harder and harder to manage the costs of the bot at our side.\n{config.BULLET_EMOJI}You can help by donating / becoming a patron / sponsor on github ( links in the buttons )\n{config.BULLET_EMOJI} Github Repository, Website, Support Server will all remain active even after the bot goes down. \n\n\n**THANKS FOR BEING A PART OF AERIAL ACE FAMILY <33**"

        await ctx.send(embed=embd, view=view)

# Mail reminder
async def process_mail(ctx):

        prob : int = 100
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title=f"{config.ALERT_EMOJI} NOTICE {config.ALERT_EMOJI}", color=config.NORMAL_COLOR)
            embd.description = f"Aerial Ace is going to be discontinued from 25th November 2022."
            try:
                embd.set_footer(text=f"Check the complete mail using {ctx.prefix}mail")
            except:
                pass # Dont add footer in mail reminder through slash commands

            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)