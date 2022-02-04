from discord import Embed, ApplicationContext, AutocompleteContext
from discord.ext import commands
from discord.commands import slash_command, Option

import config
from cog_helpers import tag_helper

class TagSystemSlash(commands.Cog):

    """For registering tags"""

    @slash_command(name="tag", description="Add yourself to any tag", guild_ids=[751076697884852389])
    async def assign_tag(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        reply = await tag_helper.register_tag(ctx.guild.id, ctx.author, tag)
        await ctx.respond(reply)

    """For pinging user assigned to tag"""

    @slash_command(name="pingtag", description="Ping users assigned to the provided tag", guild_ids=[751076697884852389])
    async def tag_ping(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

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

    @slash_command(name="viewtag", description="View users assigned to provided tag", guild_ids=[751076697884852389])
    async def view_tag(self, ctx, tag : Option(str, description="Name of the tag", required=True)):

        hunters = await tag_helper.get_tag_hunters(ctx.guild.id, tag)

        embd = Embed(title=f"{tag.capitalize()}", color=config.NORMAL_COLOR)
        embd.description = f"Users assigned to `{tag.capitalize()}` tag : "
        if hunters is None:
            await ctx.respond(f"No one is assigned to `{tag}` tag. \n")
            return
        else:
            for h in hunters:
                embd.description += f"<@{h}> \n"
            
            await ctx.respond(embed=embd)

    """For toggling afk"""

    states = ["on", "off"]

    async def get_afk_state(self, ctx : AutocompleteContext):
        return [state for state in self.states if state.startswith(ctx.value.lower())]

    @slash_command(name="afk", description="Change your ping status", guild_ids=[751076697884852389])
    async def afk(self, ctx : ApplicationContext, state : Option(str, "Pick a state", autocomplete=get_afk_state)):

        reply = await tag_helper.set_afk(str(ctx.guild.id), str(ctx.author.id), state)

        await ctx.respond(reply)

def setup(bot : commands.Bot):
    bot.add_cog(TagSystemSlash())