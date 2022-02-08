from discord.ext import commands
from os import listdir

from managers import mongo_manager

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

def setup(bot):
    bot.add_cog(AdminSystem(bot))