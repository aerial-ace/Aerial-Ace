from discord import File, User, Bot, Embed, Forbidden, HTTPException
from discord.ext import commands
from os import listdir
import logging

from views.ButtonViews import DonationView
from managers import mongo_manager
from helpers import battle_helper, general_helper
from config import NORMAL_COLOR, AVATAR_LINK


class AdminSystem(commands.Cog):
    bot: commands.Bot = None

    def __init__(self, bot):
        self.bot = bot

    """Show Data of any document from mongodb database"""

    @commands.is_owner()
    @commands.command(name="show_data", aliases=["sd"])
    async def show_data(self, ctx, collection: str, server_id: str):
        query = {"server_id": server_id}

        try:
            mongo_cursor = await mongo_manager.manager.get_all_data(collection, query)
        except Exception as e:
            await ctx.reply(f"```{e}```")
            return

        try:
            data = mongo_cursor[0]
        except Exception as e:
            await ctx.reply(f"```{e}```")
            return

        reply = f"""
        __{collection.capitalize()}'s data__ in {server_id}
        ```
        {str(data)}
        ```
        """

        await ctx.send(reply)

    """Unload any cog"""

    @commands.is_owner()
    @commands.command(name="unload")
    async def unload_cog(self, ctx: commands.Context, cog):

        bot: commands.Bot = ctx.bot

        if cog == "slash":
            return await ctx.send(await self.toggle_slash_cogs(True))

        try:
            bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"Unable to unload that cog.\n **Error** : {e}")
        else:
            await ctx.send(f"Cog unloaded successfully : `{cog}`")

    """Load any cog"""

    @commands.is_owner()
    @commands.command(name="load")
    async def load_cog(self, ctx: commands.Context, cog):

        bot: commands.Bot = ctx.bot

        if cog == "slash":
            return await ctx.send(await self.toggle_slash_cogs(False))

        try:
            bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Unable to unload that cog.\n **Error** : {e}")
        else:
            await ctx.send(f"Cog loaded successfully : `{cog}`")

    """Toggle Slash Commands"""

    async def toggle_slash_cogs(self, unload=True) -> str:

        if unload is True:
            try:
                for file in listdir("./cogs/slash"):
                    if file.endswith(".py"):
                        self.bot.unload_extension(f"cogs.slash.{file[:-3]}")
            except Exception as e:
                return f"Error occurred while unloading slash commands : {e}"
            else:
                return "Slash cogs unloaded successfully"
        else:
            try:
                for file in listdir("./cogs/slash"):
                    if file.endswith(".py"):
                        self.bot.load_extension(f"cogs.slash.{file[:-3]}")
            except Exception as e:
                return f"Error occurred while loading slash commands : {e}"
            else:
                return "Slash cogs loaded successfully"

    """Disable Command"""

    @commands.command(name="disable", aliases=["disable_cmd"])
    @commands.is_owner()
    async def disable_command(self, ctx: commands.Context, cmd: str):
        try:
            bot: commands.Bot = ctx.bot
            bot.get_command(cmd).enabled = False
        except Exception as e:
            await ctx.send(f"Error while trying to disable the command!\n {e}")
        else:
            await ctx.send(f"Command `{cmd}` was disabled successfully!")

    """Enable Command"""

    @commands.command(name="enable", aliases=["enable_cmd"])
    @commands.is_owner()
    async def enable_command(self, ctx: commands.Context, cmd: str):
        try:
            bot: commands.Bot = ctx.bot
            bot.get_command(cmd).enabled = True
        except Exception as e:
            await ctx.send(f"Error while trying to enable the command!\n {e}")
        else:
            await ctx.send(f"Command `{cmd}` was enabled successfully!")

    """All commands"""

    @commands.command(name="all_commands", aliases=["all", "all_cmds"],
                      description="Returns a list of all commands available in the bot.")
    async def all_commands(self, ctx: commands.Context):

        embd = Embed(title="All Commands - Aerial Ace", color=NORMAL_COLOR)
        embd.description = ""

        bot: commands.Bot = ctx.bot
        all_cmds = [[cmd.name, cmd.enabled] for cmd in list(bot.commands)]
        numb_of_cmds = len(all_cmds)
        cmds_per_line = int(len(all_cmds) / 3)

        strs = []

        for i in range(0, int(numb_of_cmds / cmds_per_line)):
            string = ""
            for j in range(cmds_per_line):
                this_command = all_cmds[i * cmds_per_line + j]
                string += this_command[0]
                string += (" - :x:" if this_command[1] is False else "")
                string += "\n"

            strs.append(string)

        embd.add_field(
            name="Page-1",
            value=strs[0],
            inline=True
        )

        embd.add_field(
            name="Page-2",
            value=strs[1],
            inline=True
        )

        embd.add_field(
            name="Page-3",
            value=strs[2],
            inline=True
        )

        await ctx.send(embed=embd)

    @commands.command(name="tier", aliases=["set_tier"], description="Updates the Tier of the provided server")
    @commands.is_owner()
    async def set_tier(self, ctx: commands.Context, server_id: int, tier: int):

        query = {
            "server_id": str(server_id)
        }

        updated_data = {
            "tier": tier
        }

        try:
            await mongo_manager.manager.update_all_data("servers", query, updated_data)
        except Exception as e:
            await ctx.send(f"Error! ```{e}```")
        else:
            await ctx.send(f"Server with id **{server_id}** is now at **Tier {tier}**")

    @commands.command(name="view_blb", aliases=["vblb"])
    async def view_blb(self, ctx: commands.Context, guild_id: str):

        paginator = await battle_helper.get_battle_leaderboard_paginator(id=guild_id)

        await paginator.send(ctx)
    
    @commands.is_owner()    
    @commands.command(name="setvalue", aliases=["sv"], description="Set the value of a key in database")
    async def set_value(self, ctx: commands.Context, server_id:str, key:str, value:str):
        
        key_tree = key.split(".")
        
        collection = key_tree[0]
        
        query = {
            "server_id" : server_id
        }
        
        updated_data = {
            ".".join(key_tree[1:]) : value
        }
        
        try:
            await mongo_manager.manager.update_all_data(collection, query, updated_data)
        except Exception as e:
            embd:Embed = await general_helper.get_error_embd("ERROR OCCURRED!", desc="")
            embd.description = "```-aa sv <server_id> <collection>.<key1>.<key2>...<keyn> <value>```"
            
            return await ctx.send(embed=embd)
        else:
            await ctx.send("Value Updated!")

    @commands.is_owner()
    @commands.command(name="logs", aliases=["get-logs", "gl"], description="returns the latest log file")
    async def get_logs(self, ctx:commands.Context):
       with open("logs/aerial-ace.log", 'r') as log_file:
            await ctx.send("Here is the log file:", file=File(log_file, "aerial-ace.log"))

    @commands.command(name="send-reminder", aliases=["send-rem"], description="Send a premium reminder to the owner")
    async def send_reminder(self, ctx:commands.Context, user_id:str, *, server_id:str):

        server_ids = server_id.split()

        bot:Bot = ctx.bot
        premium_user:User = await bot.fetch_user(user_id)

        if premium_user is None:
            return await ctx.send(f"User with ID : _{user_id}_ was not found!")

        server_list = []

        for i in server_ids:
            gld = await bot.fetch_guild(int(i))

            server_list.append(
                {
                    "name" : gld.name,
                    "id" : gld.id
                }
            )

        premium_reminder_embd:Embed = Embed(title="REMINDER!", description="", color=NORMAL_COLOR)
        premium_reminder_embd.set_thumbnail(url=AVATAR_LINK)
        premium_reminder_embd.description = "This is a reminder that patreon has restricted access to the premium features of the Aerial Ace bot for the below mentioned server(s)\n"

        for i in server_list:
            server_name = i.get("name")
            server_id = i.get("id")
            premium_reminder_embd.description += f"\nName : **{server_name}**, ID : **{server_id}**"

        premium_reminder_embd.description += "\n\nPlease make sure you clear your payment via patreon ( or any other payment method you are using ) to keep the premium features and priority support."
        premium_reminder_embd.description += "\n\nIn case you are having difficulty in the payment process, please contact the dev. at the support server."

        try:
            if premium_user.can_send("Premium Check!"):
                await premium_user.send(embed=premium_reminder_embd, view=DonationView(timeout=600))
            else:
                await ctx.send("Can't send premium notification")

        except Forbidden:
            return await ctx.send("User has `Receive Messages` disabled!")
        except HTTPException as e:
            logging.error(f"Error while sending reminder embed! ```{e}```")
            return await ctx.send(f"Some Error occurred while sending DM to the user!\n```{e}```")

def setup(bot):
    bot.add_cog(AdminSystem(bot))
