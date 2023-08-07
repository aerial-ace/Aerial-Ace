from discord.ext import commands
from discord import TextChannel, Member, Embed, Interaction

from views.ButtonViews import AcceptanceView
from helpers import donation_helper

class DonationModule(commands.Cog):

    @commands.group(name="donation", aliases=["dono"], description="Parent command for all the donation related commands.")
    async def donation(self, context:commands.Context):
        if context.subcommand_passed is None:
            
            reply = await donation_helper.get_donation_information_embed(context.guild)

            await context.send(embed=reply)
        
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

    @donation.command(name="staff", description="Change the staff role ID.")
    async def staff(self, context:commands.Context, role_id:int):

        if context.author.id != context.guild.owner.id:
            return await context.reply("This command can only be run by server owner!")
        
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

        def decline_callback():
            return False

        await context.send(embed=confirmation, view=AcceptanceView(200, acceptance_callback, decline_callback))

    @change.error
    async def change_error_handler(self, context:commands.Context, error):

        if isinstance(error, commands.errors.BadArgument) or isinstance(error, commands.errors.TooManyArguments):
            await context.reply("The parameters must follow this structure : \n`-aa donation change <user-id> <pokecoins> <shinies> <rares> <redeems>`")


def setup(bot : commands.Bot):
    bot.add_cog(DonationModule())