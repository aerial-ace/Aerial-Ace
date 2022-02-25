from discord.ext import commands
from discord import Member

from config import ERROR_COLOR, WARNING_COLOR
from cog_helpers import tag_helper
from cog_helpers import general_helper
from managers import cache_manager

class TagSystem(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # validates a tag 
    async def validate_tag(self, ctx : commands.Context, tag) -> bool:
        try:
            cache_manager.cached_type_data[tag.lower()]
        except KeyError as keyErr:
            reply = await general_helper.get_info_embd("Not Found Error!", f"`{tag.capitalize()}` is not a pokemon name, atleast in english\nPlease provide valid pokemon names in english.", ERROR_COLOR)
            await ctx.send(embed=reply)
            return False
        else:
            return True

    """Assign tags"""

    @commands.guild_only()
    @commands.command()
    async def tag(self, ctx, tag : str):
        
        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        await ctx.send(reply)

    @tag.error
    async def tag_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"> Gib a tag name when? Like this ```{ctx.prefix}tag Ralts```")
        else:
            await ctx.send(error)

    """Ping tags"""

    @commands.guild_only()
    @commands.command(name="tag_ping", aliases=["tp"])
    async def tag_ping(self, ctx, tag: str):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)

        if hunters is None:
            reply = await general_helper.get_info_embd("Tag not found", "No one is assigned to `{tag}` tag".format(tag=tag.capitalize()), WARNING_COLOR)
            await ctx.send(embed=reply)
            return

        number_of_hunters = len(hunters)
        pings = ""

        for i in range(0, number_of_hunters):
            pings = pings + f"<@{str(hunters[i])}>"
            if i <= number_of_hunters - 2:
                pings += " | "

        await ctx.send(f"Pinging users assigned to `{tag.capitalize()}` tag\n\n{pings}")

    @tag_ping.error
    async def tag_ping_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a tag as a parameter.\n```{ctx.prefix}tag_ping Espurr```", ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

    """View tags"""

    @commands.guild_only()
    @commands.command(name="tag_show", aliases=["ts"])
    async def tag_show(self, ctx, tag : str):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)

        if hunters is None:
            reply = await general_helper.get_info_embd("Tag not found", "No one is assigned to `{tag}` tag".format(tag=tag.capitalize()), WARNING_COLOR)
            await ctx.reply(embed=reply)
            return

        reply = await tag_helper.get_show_hunters_embd(tag, hunters)

        await ctx.send(embed=reply)

    @tag_show.error
    async def tag_show_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a tag as a parameter.\n```{ctx.prefix}tag_show Darumaka```", ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

    """Remove tags"""

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(name="tag_remove", aliases=["tr"])
    async def tag_remove(self, ctx, user : Member):
        reply = await tag_helper.remove_user(ctx.guild.id, user)
        await ctx.send(reply)

    @tag_remove.error
    async def tag_remove_helper(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a user as a parameter.\n```{ctx.prefix}tag_remove @shit_guy_69```", ERROR_COLOR)
            await ctx.reply(embed=reply)
        elif isinstance(error, commands.errors.MissingPermissions):
            reply = "Be a Admin when?"
            await ctx.reply(reply)
        else:
            await ctx.send(error)

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(name="tag_remove_id", aliases=["trid"])
    async def tag_remove_id(self, ctx, user_id : str):
        reply = await tag_helper.remove_user_id(ctx.guild.id, user_id)
        await ctx.send(reply)

    @tag_remove_id.error
    async def tag_remove_id_helper(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a user_id as a parameter.\n```{ctx.prefix}tag_remove_id 716390085896962058```", ERROR_COLOR)
            await ctx.reply(embed=reply)
        elif isinstance(error, commands.errors.MissingPermissions):
            reply = "Be a Admin when?"
            await ctx.reply(reply)
        else:
            await ctx.send(error)

    """Set afk"""

    @commands.guild_only()
    @commands.command()
    async def afk(self, ctx, state):

        if state.lower() not in ["on", "off"]:
            return

        reply = await tag_helper.set_afk(str(ctx.guild.id), str(ctx.author.id), state.lower())
        await ctx.send(reply)

    @afk.error
    async def afk_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires `State` as a parameter. Like this```{ctx.prefix}afk on [off]```", color=ERROR_COLOR)
            await ctx.reply(embed=reply)
            return

        await ctx.send(error)

def setup(bot):
    bot.add_cog(TagSystem(bot))