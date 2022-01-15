from discord.ext import commands

from cog_helpers import tag_helper

class TagSystem(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command()
    async def tag(self, ctx, tag : str):
        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        await ctx.send(reply)

    @tag.error
    async def tag_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply("> Gib a tag name when? Like this ```>>tag Ralts```")
        else:
            await ctx.send(error)

    @commands.guild_only()
    @commands.command(name="tag_ping", aliases=["tp"])
    async def tag_ping(self, ctx, tag: str):
        hunters = await tag_helper.get_tag_hunters(str(ctx.guild.id), tag)

        if hunters is None:
            await ctx.send(f"No one is assigned to `{tag.capitalize()}` tag")
            return
        
        pings = ""

        for hunter in hunters:
            pings += f"<@{hunter}>"

        await ctx.send(f"Pinging users assigned to `{tag.capitalize()}` \n{pings}")

def setup(bot):
    bot.add_cog(TagSystem(bot))