from discord.ext import commands
from discord import Embed
from os import listdir

from managers import mongo_manager
from config import NORMAL_COLOR, DEVELOPER_EMOJI

class AdminSystem(commands.Cog):

    bot : commands.Bot = None

    def __init__(self, bot):        
        self.bot = bot

    """Show Data of any document from mongodb database"""

    @commands.is_owner()
    @commands.command(name="show_data", aliases=["sd"])
    async def show_data(self, ctx, collection : str, server_id : str):
        query = {"server_id" : server_id}

        try:
            mongo_cursor = mongo_manager.manager.get_all_data(collection, query)
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
    async def unload_cog(self, ctx : commands.Context, cog):

        bot : commands.Bot = ctx.bot

        if cog == "slash":
            return await ctx.send( await self.toggle_slash_cogs(True))

        try:
            bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f"Unable to unload that cog.\n **Error** : {e}")
        else:
            await ctx.send(f"Cog unloaded successfully : `{cog}`")

    """Load any cog"""

    @commands.is_owner()
    @commands.command(name="load")
    async def load_cog(self, ctx : commands.Context, cog):

        bot : commands.Bot = ctx.bot

        if cog == "slash":
            return await ctx.send( await self.toggle_slash_cogs(False))

        try:
            bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f"Unable to unload that cog.\n **Error** : {e}")
        else:
            await ctx.send(f"Cog loaded successfully : `{cog}`")

    """Toggle Slash Commands"""

    async def toggle_slash_cogs(self, unload = True) -> str:
        
        if unload is True:
            try:
                for file in listdir("./cogs/slash"):
                    if file.endswith(".py"):
                        self.bot.unload_extension(f"cogs.slash.{file[:-3]}")
            except Exception as e:
                return f"Error occured while unloading slash commands : {e}"
            else:
                return "Slash cogs unloaded successfully"
        else:
            try:
                for file in listdir("./cogs/slash"):
                    if file.endswith(".py"):
                        self.bot.load_extension(f"cogs.slash.{file[:-3]}")
            except Exception as e:
                return f"Error occured while loading slash commands : {e}"
            else:
                return "Slash cogs loaded successfully"

    """Disable Command"""

    @commands.command(name="disable", aliases=["disable_cmd"])
    @commands.is_owner()
    async def disable_command(self, ctx:commands.Context, cmd:str):
        try:
            bot:commands.Bot = ctx.bot
            bot.get_command(cmd).enabled = False
        except Exception as e:
            await ctx.send(f"Error while trying to disable the command!\n {e}")
        else:
            await ctx.send(f"Command `{cmd}` was disabled successfully!")

    """Enable Command"""

    @commands.command(name="enable", aliases=["enable_cmd"])
    @commands.is_owner()
    async def enable_command(self, ctx:commands.Context, cmd:str):
        try:
            bot:commands.Bot = ctx.bot
            bot.get_command(cmd).enabled = True
        except Exception as e:
            await ctx.send(f"Error while trying to enable the command!\n {e}")
        else:
            await ctx.send(f"Command `{cmd}` was enabled successfully!")

    """All commands"""

    @commands.command(name="all_commands", aliases=["all", "all_cmds"], description="Returns a list of all commands available in the bot.")
    async def all_commands(self, ctx:commands.Context):

        embd = Embed(title="All Commands - Aerial Ace", color=NORMAL_COLOR)
        embd.description = ""

        bot:commands.Bot = ctx.bot
        all_cmds = [[cmd.name, cmd.enabled] for cmd in list(bot.commands)]
        numb_of_cmds = len(all_cmds)
        cmds_per_line = int(len(all_cmds) / 3)

        strs = []

        for i in range(0, int(numb_of_cmds / cmds_per_line)):
            str = ""
            for j in range(cmds_per_line):
                this_command = all_cmds[i * cmds_per_line + j]
                str += this_command[0]
                str += (" - :x:" if this_command[1] == False else "") 
                str += "\n"

            strs.append(str)

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

def setup(bot):
    bot.add_cog(AdminSystem(bot))