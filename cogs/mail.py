import discord
from discord.ext import commands
import random

import config

class MailModule(commands.Cog):
    @commands.guild_only()
    @commands.command(name="mail", aliases=["ml"])
    async def open_mail(self, ctx):

        """View all the mails in the mail box"""

        embd = discord.Embed(title="__Mail Box - Aerial Ace__", color=config.NORMAL_COLOR)
        embd.description = "Available Mails are shown here, mails keep you updated with all the new bug fixes and features in the bot"

        embd.add_field(
            name="FIX : Battle leaderboard",
            value=f"Battle leaderboard, previously broken is now fixed. Use `{ctx.prefix}blb` to view it",
            inline=False
        )
        
        embd.add_field(
            name="Fun Commands Module",
            value=f"Commands like `{ctx.prefix}kill` and `{ctx.prefix}hit` are now available. ||Totally not inspired by owo||",
            inline=False
        )

        embd.add_field(
            name="Bot Latency",
            value=f"Check the bots ping using `{ctx.prefix}ping`",
            inline=False
        )

        embd.add_field(
            name="Admin Commands",
            value=f"Added commands for Admins to remove users from battleboard or from any tag. Use `{ctx.prefix}tag_remove` and `{ctx.prefix}battle_remove` commands to do remove inactive users.",
            inline=False
        )

        await ctx.send(embed=embd)

# Mail reminder
async def process_mail(ctx):

        prob : int = -1
        roll = random.randint(0, 100)

        if roll > 0 and roll < prob:
            embd = discord.Embed(title="Mail Box", color=config.NORMAL_COLOR)
            embd.description = ":email: Check the new mails using `-aa mail`"
            await ctx.send(embed=embd)

def setup(bot):
    mail_module = MailModule()
    bot.add_cog(mail_module)