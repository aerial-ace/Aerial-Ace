from discord import Member, ApplicationContext, AutocompleteContext
from discord.ext import commands
from discord.commands import slash_command, Option

from views.ButtonViews import GeneralView
from managers import cache_manager
from cog_helpers import general_helper
from cog_helpers import tag_helper
from config import ERROR_COLOR

class TagSystemSlash(commands.Cog):

    bot : commands.Bot = None

    def __init__(self, bot) -> None:
        self.bot = bot

    # validates a tag 
    async def validate_tag(self, ctx : ApplicationContext, tag) -> bool:
        try:
            cache_manager.cached_type_data[tag.lower()]
        except KeyError as keyErr:
            reply = await general_helper.get_info_embd("Not Found Error!", f"`{tag.capitalize()}` is not a pokemon name, atleast in english\nPlease provide valid pokemon names in english and that follow this format ```{ctx.prefix}dex marowak-alola\n{ctx.prefix}dex gallade-mega\n{ctx.prefix}dex meowstic-female\n{ctx.prefix}dex deoxys-defense\n{ctx.prefix}dex necrozma-dawn\n{ctx.prefix}dex calyrex-shadow-rider\n{ctx.prefix}dex cinderace-gmax```", ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)
            await ctx.respond(embed=reply, view=view)
            return False
        else:
            return True

    """For registering tags"""

    @slash_command(name="tag", description="Add yourself to any tag")
    async def assign_tag(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(reply, view=view)

    """For pinging user assigned to tag"""

    @slash_command(name="pingtag", description="Ping users assigned to the provided tag")
    async def tag_ping(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)
        view = GeneralView(200, True, True, False, True)

        if hunters is None:
            await ctx.respond(f"No one is assigned to `{tag}` tag.")
            return
        else:
            pings = ""
            for hunter in hunters:
                pings = pings + f"<@{hunter}> "

            await ctx.respond(f"Pinging user assigned to `{tag}` tag.\n\n{pings}", view=view)
    
    """For viewing users assigned to tag"""

    @slash_command(name="viewtag", description="View users assigned to provided tag")
    async def view_tag(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)

        if hunters is None:
            await ctx.respond(f"No one is assigned to `{tag}` tag.")
            return
        else:
            reply = await tag_helper.get_show_hunters_embd(tag, hunters)
            view = GeneralView(200, True, True, False, True)

            await ctx.respond(embed=reply, view=view)

    """For toggling afk"""

    states = ["on", "off"]

    async def get_afk_state(self, ctx : AutocompleteContext):
        return [state for state in self.states if state.startswith(ctx.value.lower())]

    @slash_command(name="afk", description="Change your ping status")
    async def afk(self, ctx : ApplicationContext, state : Option(str, "Pick a state", autocomplete=get_afk_state)):

        reply = await tag_helper.set_afk(str(ctx.guild.id), str(ctx.author.id), state)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(reply, view=view)

    """For clearing your tag"""
    @slash_command(name="tag-clear", description="Removes your tag", guild_ids=[751076697884852389])
    async def tag_clear(self, ctx:ApplicationContext):

        reply = await tag_helper.remove_user(ctx.guild.id, ctx.author)
        view  = GeneralView(200, True, True, False, True)

        await ctx.respond(reply, view=view)

    """For Clearing all tags in the server"""
    @slash_command(name="tag-clear-all", description="Remove all tags created in this server", guild_ids=[751076697884852389])
    async def tag_clear_all(self, ctx:ApplicationContext):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        confirmation_embed = await general_helper.get_info_embd("Are you Sure?", "This will remove all tags created in this server! Please be cautious, as this cannot be undone. Type **CONFIRM** to confirm", ERROR_COLOR)
        await ctx.respond(embed=confirmation_embed)

        bot:commands.Bot = ctx.bot

        def confirm_check(message):
            return message.author == ctx.author and message.content.lower() == "confirm"

        try:
            await bot.wait_for("message", check=confirm_check, timeout=10.0)
        except:
            return await ctx.send(embed=await general_helper.get_info_embd("Cancelled!", ""))

        reply = await tag_helper.remove_all_tags(str(ctx.guild.id))
        view  = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)


    """For removing users from their tag"""

    @slash_command(name="tag-remove", description="Remove a user from their tag")
    async def tag_remove(self, ctx : ApplicationContext, user : Option(Member, description="Member to remove from tag", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await tag_helper.remove_user(ctx.guild.id, user)
        view = GeneralView(200, True, True, False, True)
        
        await ctx.respond(reply, view=view)

    """For removing user from their tag using user id"""

    @slash_command(name="tag-remove-id", description="Remove a user from their tag using user id")
    async def tag_remove_id(self, ctx : ApplicationContext, user_id : Option(str, description="Member to remove from tag", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await tag_helper.remove_user_id(ctx.guild.id, user_id)
        view = GeneralView(200, True, True, False, True)
        
        await ctx.respond(reply, view=view)

    """All tags in the server"""
    @slash_command(name="alltags", description="View all tags in the server")
    async def view_all_tags(self, ctx:ApplicationContext):

        reply = await tag_helper.get_all_tags_embed(ctx.guild)
        view = GeneralView(200, True, True, False, True)

        await ctx.respond(embed=reply, view=view)

def setup(bot : commands.Bot):
    bot.add_cog(TagSystemSlash(bot))