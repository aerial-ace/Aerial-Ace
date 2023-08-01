from discord.ext import commands
from discord import TextChannel

from helpers import donation_helper

class DonationModule(commands.Cog):

    @commands.group(name="donation", aliases=["dono"], description="Parent command for all the donation related commands.")
    async def donation(self, context:commands.Context):
        if context.subcommand_passed is None:
            return await context.reply("Please provide a valid subcommand.")
        
    @donation.command(name="channel", aliases=["ch"], description="Change the donation channel using this command")
    async def channel(self, context:commands.Context, channel:TextChannel):

        bot:commands.Bot = context.bot

        if channel.permissions_for(context.guild.get_member(bot.user.id)).send_messages is False:
            return await context.reply("Aerial Ace isn't allowed to send messages in that channel! Please give appropriate permissions.")
        
        outcome = await donation_helper.set_channel(context.guild.id, channel.id)

        if outcome is True:
            await context.reply("Donation Channel was successfully set to {}".format(channel.mention))
        else:
            await context.reply("Some Error occurred while trying to set Donation Channel!")


def setup(bot : commands.Bot):
    bot.add_cog(DonationModule())