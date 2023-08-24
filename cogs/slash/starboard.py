from discord import TextChannel
from discord.ext import commands
from discord import ApplicationContext, Option
from discord.commands import SlashCommandGroup

from helpers import starboard_helper


class StarboardSlash(commands.Cog):
    starboard_group = SlashCommandGroup(name="starboard", description="Commands related to starboard customization")

    """Enable or Disable the starboard channel"""

    @starboard_group.command(name="channel", description="Enable/Disable Starboard Channel")
    async def set_starboard(self, ctx: ApplicationContext, channel: Option(TextChannel, description="Channel where Rare Catches will be sent", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")

        reply = await starboard_helper.set_starboard(str(ctx.guild_id), channel)
        await ctx.respond(reply)

    @starboard_group.command(name="rare-text", description="Customize the Rare Catch Text")
    async def set_rare_text(self, ctx: ApplicationContext, text: Option(str, description="Text", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild_id), text, "RARE")

        await ctx.respond(embed=reply)

    @starboard_group.command(name="shiny-text", description="Customize the Shiny Catch Text")
    async def set_shiny_text(self, ctx: ApplicationContext, text: Option(str, description="Text", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), "DEFAULT", "SHINY")
        else:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild_id), text, "SHINY")

        await ctx.respond(embed=reply)

    @starboard_group.command(name="rare-image", description="Customize the Rare Catch Image")
    async def set_rare_text(self, ctx: ApplicationContext, text: Option(str, description="Image Link", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild_id), text, "RARE")

        await ctx.respond(embed=reply)

    @starboard_group.command(name="shiny-image", description="Customize the Shiny Catch Image")
    async def set_shiny_image(self, ctx: ApplicationContext, text: Option(str, description="Image Link", required=False, default=None)):

        if not ctx.author.guild_permissions.administrator:
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "SHINY")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild_id), text, "SHINY")

        await ctx.respond(embed=reply)


def setup(bot: commands.Bot):
    bot.add_cog(StarboardSlash())
