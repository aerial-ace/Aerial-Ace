from discord import Member, ApplicationContext, AutocompleteContext
from discord.ext import commands
from discord.commands import slash_command, Option

from config import ERROR_COLOR
from cog_helpers import general_helper
from cog_helpers import tag_helper
from managers import cache_manager

class TagSystemSlash(commands.Cog):

    bot : commands.Bot = None

    def __init__(self, bot) -> None:
        self.bot = bot

    # validates a tag 
    async def validate_tag(self, ctx : ApplicationContext, tag) -> bool:
        try:
            cache_manager.cached_type_data[tag.lower()]
        except KeyError as keyErr:
            reply = await general_helper.get_info_embd("Not Found Error!", f"`{tag.capitalize()}` is not a pokemon name, atleast in english\nPlease provide valid pokemon names in english.", ERROR_COLOR)
            await ctx.respond(embed=reply)
            return False
        else:
            return True

    """For registering tags"""

    @slash_command(name="tag", description="Add yourself to any tag")
    async def assign_tag(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        await ctx.respond(reply)

    """For pinging user assigned to tag"""

    @slash_command(name="pingtag", description="Ping users assigned to the provided tag")
    async def tag_ping(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        if await self.validate_tag(ctx, tag.lower()) is False:
            return

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)

        if hunters is None:
            await ctx.respond(f"No one is assigned to `{tag}` tag.")
            return
        else:
            pings = ""
            for hunter in hunters:
                pings = pings + f"<@{hunter}> "
            await ctx.respond(f"Pinging user assigned to `{tag}` tag.\n\n{pings}")
            return
    
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
            await ctx.respond(embed=reply)

    """For toggling afk"""

    states = ["on", "off"]

    async def get_afk_state(self, ctx : AutocompleteContext):
        return [state for state in self.states if state.startswith(ctx.value.lower())]

    @slash_command(name="afk", description="Change your ping status")
    async def afk(self, ctx : ApplicationContext, state : Option(str, "Pick a state", autocomplete=get_afk_state)):

        reply = await tag_helper.set_afk(str(ctx.guild.id), str(ctx.author.id), state)
        await ctx.respond(reply)

    """For removing users from their tag"""

    @slash_command(name="tag-remove", description="Remove a user from their tag")
    async def tag_remove(self, ctx : ApplicationContext, user : Option(Member, description="Member to remove from tag", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await tag_helper.remove_user(ctx.guild.id, user)
        await ctx.respond(reply)

    """For removing user from their tag using user id"""

    @slash_command(name="tag-remove-id", description="Remove a user from their tag using user id")
    async def tag_remove(self, ctx : ApplicationContext, user_id : Option(str, description="Member to remove from tag", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await tag_helper.remove_user_id(ctx.guild.id, user_id)
        await ctx.respond(reply)

def setup(bot : commands.Bot):
    bot.add_cog(TagSystemSlash(bot))