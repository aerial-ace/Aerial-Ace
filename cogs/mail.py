import discord
from discord.ext import commands

import config

class MailModule(commands.Cog):

    state : bool = False

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

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(name="mail_state")
    async def set_mail_state(self, ctx, state):
        if state.lower() == "on":
            self.state = True
        elif state.lower() == "off":
            self.state = False
        else:
            raise commands.errors.BadArgument()

    @set_mail_state.error
    async def set_mail_state_handler(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.reply("Gib On/Off as a parameter too :/")
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.reply("Be owner of this bot when :>")
        else:
            await ctx.reply(error)

mail_module = None

# Mail reminder
async def process_mail(ctx):

        embd = discord.Embed(title="Mail Box", color=config.NORMAL_COLOR)
        embd.description = ":email: Check the new mails using `-aa mail`"
        await ctx.send(embed=embd)

def setup(bot):
    global mail_module

    mail_module = MailModule()
    bot.add_cog(mail_module)