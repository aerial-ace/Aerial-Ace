from discord.ext import commands
from discord import TextChannel, Member, Embed, Interaction, Message
from discord import message_command, ApplicationContext

from views.ButtonViews import AcceptanceView
from helpers import donation_helper
from config import ACCEPTED_EMOJI

import pdb

class DonationModule(commands.Cog):

    @commands.group(name="donation", aliases=["dono"], description="Parent command for all the donation related commands.")
    async def donation(self, context:commands.Context):
        if context.subcommand_passed is None:
            
            reply = await donation_helper.get_donation_information_embed(context.guild)

            await context.send(embed=reply)
        
    @donation.command(name="channel", aliases=["ch"], description="Change the donation channel using this command")
    async def channel(self, context:commands.Context, channel:TextChannel=None):

        bot:commands.Bot = context.bot

        if channel is not None:
            if channel.permissions_for(context.guild.get_member(bot.user.id)).send_messages is False:
                return await context.reply("Aerial Ace isn't allowed to send messages in that channel! Please give appropriate permissions.")
                
            outcome = await donation_helper.set_channel(context.guild.id, channel.id)
        else:
            outcome = await donation_helper.set_channel(context.guild.id, None)

        if outcome is True:
            await context.reply("Donation Channel was successfully set to {}".format(channel.mention))
        else:
            await context.reply("Some Error occurred while trying to set Donation Channel!")

    @donation.command(name="staff", description="Change the staff role ID.")
    async def staff(self, context:commands.Context, role_id:int):

        # TODO : Owner Only Command
        if context.author.id != context.guild.owner_id:
            return await context.reply("This command can only be run by server owner!", ephemeral=True)
        
        if await donation_helper.set_staff_role(context.guild.id, role_id):
            return await context.send("Donation Staff Role ID is now set to `{}`".format(role_id))
        else:
            return await context.send("Error Occurred!")

    @donation.command(name="leaderboard", aliases=["lb"], description="Returns the top server donators")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, context:commands.Context):

        embd = await donation_helper.get_donation_leaderboard_embed(context.guild)

        await context.send(embed=embd)

    @donation.command(name="change", description="Change the donation values of a certain member")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def change(self, context:commands.Context, target:Member, pokecoins, shinies=None, rares=None, redeems=None):

        confirmation = Embed(title="Confirm?")

        confirmation.add_field( 
            name="Pokecoins",
            value=pokecoins,
            inline=True
        )

        confirmation.add_field(
            name="Shinies",
            value=shinies,
            inline=True
        )

        confirmation.add_field(
            name="Rares",
            value=rares,
            inline=True
        )

        confirmation.add_field(
            name="Redeems",
            value=redeems,
            inline=True
        )

        async def acceptance_callback(interaction:Interaction) -> bool:
            
            nonlocal context, target, pokecoins, shinies, rares, redeems

            if interaction.user != context.author:
                await interaction.response.send_message("This is not your command!", ephemeral=True)
                return False

            await interaction.response.defer()

            outcome = await donation_helper.change_donation_values(context.guild, target, pokecoins, shinies, rares, redeems)

            if outcome:
                await context.send("Changes Made!")
                return True
            else:
                await context.reply("Error Occurred while trying to make changes!")
                return False

        async def decline_callback(interaction:Interaction):
            return False

        await context.send(embed=confirmation, view=AcceptanceView(200, acceptance_callback, decline_callback))

    @change.error
    async def change_error_handler(self, context:commands.Context, error):

        if isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.TooManyArguments):
            await context.reply("The parameters must follow this structure : \n`-aa donation change <user-id> <pokecoins> <shinies> <rares> <redeems>`")

    @donation.command(name="log", aliases=["lc"], description="Change the log channel")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def log_channel(self, context:commands.Context, log_channel:TextChannel):

        bot_member = context.guild.get_member(context.bot.user.id)

        if log_channel.permissions_for(bot_member).send_messages is False:
            return await context.send("Not allowed to send messages in {}! Check Permissions.".format(log_channel.mention))

        await donation_helper.set_log_channel(context.guild.id, log_channel.id)

        await context.reply("Log Channel Updated!")

    @donation.command(name="clear", description="Clears the battle leaderboard.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def leaderboard_clear(self, context:commands.Context):
        
        async def acceptance_callback(interaction:Interaction):
            await interaction.response.defer()

            outcome = await donation_helper.clear_leaderboard(context.guild.id)

            if outcome:
                await interaction.response.send_message("Donation Leaderboard Cleared")
                return True
            else:
                await interaction.response.send_message("Error Occurred!")
                return False

        async def decline_callback(interaction:Interaction):
            return False

        embd = Embed(title="Are you sure?", description="This change is irreversible!")

        await context.reply(embed=embd, view=AcceptanceView(200, acceptance_callback, decline_callback))

    @donation.command(name="remove", aliases=["rm"], description="Remove a member from the leaderboard.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def leaderboard_remove(self, context:commands.Context, target:Member):

        outcome = await donation_helper.remove_user(context.guild.id, target.id)

        if outcome:
            return await context.reply("{} has been removed from the leaderboard.".format(target.mention))
        else:
            return await context.reply("Error occurred while trying to remove the user.")
        
    @message_command(name="Collected")
    async def collect(self, ctx: ApplicationContext, message:Message):

        if message.author != ctx.bot.user or len(message.embeds) <= 0:
            return await ctx.respond("This is not a Log Message! Please use this command on a Log Message to the donation as collected!", ephemeral=True)

        # TODO : Owner Only Command
        if ctx.author.id != ctx.guild.owner_id:
            return await ctx.respond("This command can only be used by the server owner!", ephemeral=True)

        main_embd = message.embeds[0]

        if main_embd.title != "Donation Log":
            return await ctx.respond("This is not a Log Message! Please use this command on a Log Message to the donation as collected!", ephemeral=True)

        main_embd.set_field_at(2, name="Status", value=f"{ACCEPTED_EMOJI} Collected", inline=True)

        await ctx.interaction.response.defer(ephemeral=True)

        await message.edit(embed=main_embd)

        await ctx.interaction.followup.send("Marked as Collected!", ephemeral=True)

    """
    
    @message_command(name="Not Collected")
    async def not_collect(self, ctx: ApplicationContext, message:Message):

        if message.author != ctx.bot.user or len(message.embeds) <= 0:
            return await ctx.respond("This is not a Log Message! Please use this command on a Log Message to the donation as collected!", ephemeral=True)

        # TODO : Owner Only Command
        # if ctx.author.id != message.guild.owner.id:
        #     return await ctx.respond("This command can only be used by the server owner!")

        main_embd = message.embeds[0]

        if main_embd.title != "Donation Log":
            return await ctx.respond("This is not a Log Message! Please use this command on a Log Message to the donation as collected!", ephemeral=True)

        main_embd.set_field_at(2, name="Status", value=f"{INFO_EMOJI} Not Collected", inline=True)

        await ctx.interaction.response.defer(ephemeral=True)

        await message.edit(embed=main_embd)

        await ctx.interaction.followup.send("Marked as Collected!", ephemeral=True)

    """

def setup(bot : commands.Bot):
    bot.add_cog(DonationModule())