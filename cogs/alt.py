import pdb
from discord.ext import commands
from discord import User

from helpers import alt_helper
from helpers import general_helper

class AltModule(commands.Cog):

    def __init__(self) -> None:
        pass

    @commands.group(name="alt", description="Home to all the alt module commands")
    async def alt(self, context:commands.Context):

        if context.subcommand_passed is None:
            return await context.reply("Please provide a valid subcommand")
        
    @alt.command(name="type", description="Used to set the type of account")
    async def type(self, context:commands.Context, type:str):

        response = False

        if type == "main" or type == "m":
            response = await alt_helper.register_account(str(context.author.id), "main")
        elif type == "alt" or type == "a":
            response = await alt_helper.register_account(str(context.author.id), "alt")
        
        if type not in ["main", "m", "alt", "a"] or response == False:
            return await context.send(embed = await general_helper.get_error_embd("Error Occurred!", "Please provide a valid type. \nEither `main` or `alt`"))
        else:
            return await context.send("Account Modified. Type set to **{}**".format(type))
        
    @alt.command(name="addmain", description="Sets your main account")
    async def add_main(self, context:commands.Context, main_account:User):

        response = await alt_helper.set_main(str(context.author.id), str(main_account.id))

        if response == -1:
            return await context.send(embed = await general_helper.get_error_embd("Error Occurred!", "Some error occurred while trying to set main account! Please report it at the official server."))

        if response == 1:
            reply_embd = await general_helper.get_info_embd(
                title="Account Modified!",
                desc=f"## Changes : \n1. Account type was set to 'ALT'\n2. Request sent to <@{main_account.id}>",
                footer="Log into main account to accept!"
            )
        else:
            reply_embd = await general_helper.get_error_embd(
                title="Not Found!",
                desc=f"Register <@{main_account.id}> as a **MAIN** account first!"
            )

        return await context.send(embed=reply_embd)
    
    @alt.command(name="regulate", aliases=["reg"], description="Satisfy all the account status in this server.")
    async def satisfy(self, context:commands.Context):

        response = await alt_helper.satisfy_status(str(context.author.id), context.guild)

        if response["response_code"] == 0:
            reply_embd = await general_helper.get_info_embd(
                title="Not Found",
                desc="No Alt Accounts were found! Link alt accounts first!"
            )
        elif response["response_code"] == 1:
            reply_embd = await general_helper.get_info_embd(
                title="Success!",
                desc="All Account Status Satisfied!\n## Modified Accounts :\n 1. <@{main_id}> - `MAIN`\n{alt_list}".format(main_id=response["out"]["main"], alt_list="\n".join([f"{pos + 2}. <@{user_id}> - `ALT`" for pos, user_id in enumerate(response["out"]["alts"])]))
            )

        return await context.send(embed=reply_embd)
    
    @alt.command(name="role", description="Change the role which is given to alt accounts")
    async def role(self, context:commands.Context, role_id:str):

        response = await alt_helper.update_role(str(context.guild.id), role_id)

        if response == -1:
            reply_embd = await general_helper.get_error_embd(
                title="Error Occurred",
                desc="Unable to update vales!"
            )
        elif response == 1:
            reply_embd = await general_helper.get_info_embd(
                title="Success!",
                desc=f"Alt Role is now set to <@&{role_id}>"
            )

        await context.send(embed=reply_embd)

def setup(bot:commands.Bot):
    bot.add_cog(AltModule())