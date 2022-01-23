from discord.ext import commands

from managers import mongo_manager

class AdminSystem(commands.Cog):
    def __init__(self, bot):        
        self.bot = bot

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


def setup(bot):
    bot.add_cog(AdminSystem(bot))