from discord.ext import commands
from discord import Member, Message
import asyncio

from views.ButtonViews import GeneralView
from managers import cache_manager
from cog_helpers import tag_helper
from cog_helpers import general_helper
from config import ERROR_COLOR, WARNING_COLOR, MAX_TAG_TIMER_VALUE

class TagSystem(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # validates a tag 
    async def validate_tag(self, ctx : commands.Context, tag) -> bool:
        try:
            cache_manager.cached_type_data[tag.lower()]
        except KeyError as keyErr:
            reply = await general_helper.get_info_embd("Not Found Error!", f"`{tag.capitalize()}` is not a pokemon name, atleast in english\nPlease provide valid pokemon names in english.", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)
            await ctx.send(embed=reply, view=view)
            return False
        else:
            return True

    """Assign tags"""

    @commands.guild_only()
    @commands.command(name="tag", description="Assign yourself to a shiny hunt tag")
    async def tag(self, ctx, tag : str):
        
        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        view = GeneralView(200, True, True, False, True)
        await ctx.send(reply, view=view)

    @tag.error
    async def tag_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.reply(f"> Gib a tag name when? Like this ```{ctx.prefix}tag Ralts```")
        

    """Ping tags"""

    @commands.guild_only()
    @commands.command(name="tag_ping", aliases=["tp"], description="Ping users assigned to a particular tag")
    async def tag_ping(self, ctx:commands.Context, tag: str):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        data = await tag_helper.get_tag_data(ctx.guild.id, tag)

        if len(data.hunters) == 0:
            reply = await general_helper.get_info_embd("Tag not found", "No one is assigned to `{tag}` tag".format(tag=tag.capitalize()), WARNING_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.send(embed=reply, view=view)
            return

        # Ping the assigned users

        pings = ["<@{}>".format(user_id) for user_id in data.hunters]

        ping_str = " | ".join(pings)

        ping_message = await ctx.send(f"Pinging users assigned to `{tag.capitalize()}` tag\n\n{ping_str}")

        # Start the timer

        post_tag_timer_embed = await general_helper.get_info_embd("", "")

        if data.timer == 0:
            post_tag_timer_embed.title = "No Post Tag Timer Set!"
        else:
            post_tag_timer_embed.title = "⌛{}s Timer Started!".format(data.timer)

        post_tag_message:Message = await ctx.send(embed=post_tag_timer_embed, reference=ping_message)

        if data.timer == 0:
            return

        # Wait for timer to end
        await asyncio.sleep(data.timer)

        await post_tag_message.delete()

        return await ctx.send(embed=await general_helper.get_info_embd("Timer Ended", "You can catch the pokemon now."), reference=ping_message)
        
    @tag_ping.error
    async def tag_ping_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a tag as a parameter.\n```{ctx.prefix}tag_ping Espurr```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(embed=reply, view=view)
        

    """View tags"""

    @commands.guild_only()
    @commands.command(name="tag_show", aliases=["ts"], description="View users assigned to a particular tag")
    async def tag_show(self, ctx, tag : str):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_data(ctx.guild.id, tag)

        if hunters is None:
            reply = await general_helper.get_info_embd("Tag not found", "No one is assigned to `{tag}` tag".format(tag=tag.capitalize()), WARNING_COLOR)
            await ctx.reply(embed=reply)
            return

        reply = await tag_helper.get_show_hunters_embd(tag, hunters)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @tag_show.error
    async def tag_show_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a tag as a parameter.\n```{ctx.prefix}tag_show Darumaka```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(embed=reply, view=view)


    """Set the tag post timer"""

    @commands.command(name="tag_timer", aliases=["tt"], description="Sets the post tag timer for this server | Enter 0 to disable")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def tag_timer(self, ctx:commands.Context, value:str):

        try:
            value = int(value)
        except:
            await ctx.send("Enter a valid Integer between 1 and 500")
            return

        if value > MAX_TAG_TIMER_VALUE or value < 1:
            await ctx.reply("Timer Values higher than **500 seconds** are not allowed!")
            return

        reply = await tag_helper.update_timer(str(ctx.guild.id), value)
        view  = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    """Clear Personal Tag"""        
    @commands.guild_only()
    @commands.command(name="tag_clear", aliases=["tc"], description="Removes the users from his current tag.")
    async def tag_clear(self, ctx:commands.Context):
        reply = await tag_helper.remove_user(ctx.guild.id, ctx.author)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(reply, view=view)


    """Clear All Tags"""

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(name="tag_clearall", aliases=["tca"], description="Remove all users of this server from their tags")
    async def tag_clearall(self, ctx:commands.Context):

        confirmation_embed = await general_helper.get_info_embd("Are you Sure?", "This will remove all tags created in this server! Please be cautious, as this cannot be undone. Type **CONFIRM** to confirm", ERROR_COLOR)
        await ctx.reply(embed=confirmation_embed)

        bot:commands.Bot = ctx.bot

        def confirm_check(message):
            return message.author == ctx.author and message.content.lower() == "confirm"

        try:
            await bot.wait_for("message", check=confirm_check, timeout=10.0)
        except:
            return await ctx.send(embed=await general_helper.get_info_embd("Cancelled!", ""))

        reply = await tag_helper.remove_all_tags(str(ctx.guild.id))
        view  = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)


    """Remove tags"""

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(name="tag_remove", aliases=["tr"], description="Remove users from their current tag (Admins Only)")
    async def tag_remove(self, ctx, user : Member):
        reply = await tag_helper.remove_user(ctx.guild.id, user)
        view = GeneralView(200, True, True, False, True)
        await ctx.send(reply, view=view)

    @tag_remove.error
    async def tag_remove_helper(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a user as a parameter.\n```{ctx.prefix}tag_remove @shit_guy_69```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(embed=reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            reply = "Be a Admin when?"
            view = GeneralView(200, True, True, False, True)
            await ctx.reply(reply, view=view)
        
    
    """Remove Tag By User ID"""

    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.command(name="tag_remove_id", aliases=["trid"], description="Remove user from their current tag using id (Admins Only)")
    async def tag_remove_id(self, ctx, user_id : str):
        reply = await tag_helper.remove_user_id(ctx.guild.id, user_id)
        view = GeneralView(200, True, True, False, True)
        await ctx.send(reply, view=view)

    @tag_remove_id.error
    async def tag_remove_id_helper(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires a user_id as a parameter.\n```{ctx.prefix}tag_remove_id 716390085896962058```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(embed=reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            reply = "Be a Admin when?"
            await ctx.reply(reply)
        

    """Set afk"""

    @commands.guild_only()
    @commands.command(name="afk", description="Sets your afk state to on/off")
    async def afk(self, ctx, state):

        if state.lower() not in ["on", "off"]:
            return

        reply = await tag_helper.set_afk(str(ctx.guild.id), str(ctx.author.id), state.lower())
        view = GeneralView(200, True, True, False, True)
        await ctx.send(reply, view=view)

    @afk.error
    async def afk_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires `State` as a parameter. Like this```{ctx.prefix}afk on [off]```", color=ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(embed=reply, view=view)
            return

        await ctx.send(error)


    """All tags present in the server"""
    @commands.command(name="alltags", description="Returns a list of all tags in the server")
    @commands.guild_only()
    async def view_all_tags(self, ctx:commands.Context):

        reply = await tag_helper.get_all_tags_embed(ctx.guild)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(embed=reply, view=view)

    @view_all_tags.error
    async def view_all_tag_handler(self, ctx:commands.Context, error):

        await ctx.send(error)


def setup(bot):
    bot.add_cog(TagSystem(bot))