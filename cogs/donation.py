from discord.ext import commands
from discord.ext.pages import Paginator
from discord import TextChannel, Member, Embed, Interaction, Message
from discord import message_command, ApplicationContext

from views.ButtonViews import AcceptanceView
from helpers import donation_helper
from config import ACCEPTED_EMOJI, NORMAL_COLOR

class DonationModule(commands.Cog):

    @commands.group(name="donation", aliases=["dono"], description="Parent command for all the donation related commands.")
    async def donation(self, context:commands.Context):
        if context.subcommand_passed is None:
            
            reply = await donation_helper.get_donation_information_embed(context.guild)

            await context.send(embed=reply)

    """A channel where donations are logged! ( ADMIN ONLY )"""

    @donation.command(name="channel", aliases=["ch"], description="Change the donation channel using this command")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def channel(self, context:commands.Context, channel:TextChannel=None):

        bot:commands.Bot = context.bot

        if channel is not None:
            if channel.permissions_for(context.guild.get_member(bot.user.id)).send_messages is False:
                return await context.reply("Aerial Ace isn't allowed to send messages in that channel! Please give appropriate permissions.")
                
            outcome = await donation_helper.set_channel(context.guild.id, channel.id)
        else:
            outcome = await donation_helper.set_channel(context.guild.id, None)

        if outcome is True:
            await context.reply("Donation Channel was successfully set to {}".format(channel.mention) if channel is not None else "Donation Channel Removed!")
        else:
            await context.reply("Some Error occurred while trying to set Donation Channel!")

    """Set the role allowed to collect donations ( OWNER ONLY )"""

    @donation.command(name="staff", description="Change the staff role ID.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def staff(self, context:commands.Context, role_id:int):

        # owner check
        if context.author.id != context.guild.owner_id:
            return await context.reply("This command can only be run by server owner!")
        
        if await donation_helper.set_staff_role(context.guild.id, role_id):
            return await context.send("Donation Staff Role ID is now set to `{}`".format(role_id))
        else:
            return await context.send("Error Occurred!")

    """View the donation leaderboard"""

    @donation.command(name="leaderboard", aliases=["lb"], description="Returns the top server donators")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leaderboard(self, context:commands.Context):

        paginator:Paginator = await donation_helper.get_donation_leaderboard_embed(context.guild)

        await paginator.send(context)

    """Change the donation values of a user ( ADMIN ONLY )"""

    @donation.command(name="change", description="Change the donation values of a certain member")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def change(self, context:commands.Context, target:Member, pokecoins=0, shinies=0, rares=0, redeems=0):

        confirmation = Embed(title="Confirm?", description="Final Values : \n", color=NORMAL_COLOR)

        confirmation.description += "```Pokecoins : {}\nShinies : {}\nRares : {}\nRedeems : {}```".format(pokecoins, shinies, rares, redeems)

        async def acceptance_callback(interaction:Interaction) -> bool:
            
            nonlocal context, target, pokecoins, shinies, rares, redeems

            outcome = await donation_helper.change_donation_values(context.guild, target, pokecoins, shinies, rares, redeems)

            if outcome is True:
                await interaction.followup.send("Changes Made!")
                return True
            elif outcome is False:
                await interaction.followup.send("Error Occurred while trying to make changes!")
                return True
            elif outcome is None:
                await interaction.followup.send("{} doesn't exists in the leaderboard.".format(target.mention))
                return True

        async def decline_callback(interaction:Interaction):
            return True

        await context.send(embed=confirmation, view=AcceptanceView(200, context, acceptance_callback, decline_callback))

    """Change the logging channel"""

    @donation.command(name="log", aliases=["lc"], description="Change the log channel")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def log_channel(self, context:commands.Context, log_channel:TextChannel=None):

        bot_member = context.guild.get_member(context.bot.user.id)

        if log_channel is None:
            await donation_helper.set_log_channel(context.guild.id, None)
        else:
            if log_channel.permissions_for(bot_member).send_messages is False:
                return await context.send("Not allowed to send messages in {}! Check Permissions.".format(log_channel.mention))

            await donation_helper.set_log_channel(context.guild.id, log_channel.id)

        await context.reply("Log Channel Updated!")

    """Clears the leaderboard"""

    @donation.command(name="clear", description="Clears the battle leaderboard.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def leaderboard_clear(self, context:commands.Context):
        
        async def acceptance_callback(interaction:Interaction):

            outcome = await donation_helper.clear_leaderboard(context.guild.id)

            if outcome:
                await interaction.followup.send("Donation Leaderboard Cleared")
                return True
            else:
                await interaction.followup.send("Error Occurred!")
                return False

        async def decline_callback(interaction:Interaction):
            return True

        embd = Embed(title="Are you sure?", description="This change is irreversible!")

        await context.reply(embed=embd, view=AcceptanceView(200, context, acceptance_callback, decline_callback))

    """Removes the user from the leaderboard"""

    @donation.command(name="remove", aliases=["rm"], description="Remove a member from the leaderboard.")
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def leaderboard_remove(self, context:commands.Context, target:Member):

        async def accepted(interaction:Interaction):        
            outcome = await donation_helper.remove_user(context.guild.id, target.id)

            if outcome:
                await interaction.followup.send("{} has been removed from the leaderboard.".format(target.mention))
                return True
            else:
                await interaction.followup.send("Error occurred while trying to remove the user.")
                return False

        async def declined(interaction:Interaction):
            return True

        await context.send(embed=Embed(title="Are you Sure?", description="{} will be removed from the leaderboard.".format(target.mention)), view=AcceptanceView(200, context, accepted, declined))
        
    """Mark the donation as collected! ( OWNER ONLY )"""

    @message_command(name="Collected")
    async def collect(self, ctx: ApplicationContext, message:Message):

        if message.author != ctx.bot.user or len(message.embeds) <= 0:
            return await ctx.respond("This is not a Log Message! Please use this command on a Log Message to the donation as collected!", ephemeral=True)

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