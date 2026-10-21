import random

from discord import ApplicationContext, Forbidden, Option, TextChannel
from discord.commands import SlashCommandGroup
from discord.ext import commands

from helpers import general_helper, starboard_helper
from managers.logging_manager import get_logger

logger = get_logger()


class StarboardSlash(commands.Cog):
    starboard_group = SlashCommandGroup(name="starboard", description="Commands related to starboard customization")

    """Enable or Disable the starboard channel"""

    @starboard_group.command(name="channel", description="Enable/Disable Starboard Channel")
    async def set_starboard(self, ctx: ApplicationContext, channel: Option(TextChannel, description="Channel where Rare Catches will be sent", required=False, default=None)):
        if ctx.guild is None:
            return

        if not ctx.author.guild_permissions.administrator:  # pyright: ignore[reportAttributeAccessIssue]
            return ctx.respond("Be an admin when :/")

        reply = await starboard_helper.set_starboard(str(ctx.guild_id), channel)
        await ctx.respond(reply)

    """ Toggle High Res Images"""

    @starboard_group.command(name="high-res", description="Enable/Disable High-Res pokemon images in starboard message.")
    async def toggle_highres(self, ctx: ApplicationContext):
        if ctx.guild is None:
            return

        reply = await starboard_helper.set_highres(str(ctx.guild.id))

        await ctx.respond(reply)

    """ Set Alert Mask """

    @starboard_group.command(name="alert-enable", description="Enables alerts for the provided catch type!")
    async def enable_alerts(self, ctx: ApplicationContext, alert_type: Option(str, description="The type of alert to enable. Pick one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")):
        if ctx.guild is None:
            return

        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]

        if alert_type not in alert_types:
            return await ctx.respond("Not a valid alert type! Alert type can only be one from : [rare/ shiny/ hunt/ gmax/ streak]")

        reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert_type, True)

        await ctx.respond(reply)

    """ Disable Alert Mask """

    @starboard_group.command(name="alert-disable", description="Disables alerts for the provided catch type!")
    async def disable_alerts(self, ctx: ApplicationContext, alert_type: Option(str, description="The type of alert to disable. Pick one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")):
        if ctx.guild is None:
            return

        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]

        if alert_type not in alert_types:
            return await ctx.respond("Not a valid alert type! Alert type can only be one from : [rare/ shiny/ hunt/ gmax/ streak]")

        reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert_type, False)

        await ctx.respond(reply)

    """ Toggle/Set Shiny Starboard Channel """

    @starboard_group.command(name="shiny-channel", description="Set/Disables shiny channel in your server.")
    async def set_shiny_channel(seld, ctx: ApplicationContext, channel: Option(TextChannel, description="Channel to set as shiny channel.")):
        if ctx.guild is None:
            return

        reply = await starboard_helper.set_shiny_starboard(str(ctx.guild.id), channel)

        await ctx.respond(reply)

    """Change the Starboard Catch Text"""

    @starboard_group.command(name="rare-text", description="Customize the Rare Catch Text")
    async def set_rare_text(self, ctx: ApplicationContext, text: Option(str, description="Text", required=False, default=None)):
        if ctx.guild is None:
            return

        if not ctx.author.guild_permissions.administrator:  # pyright: ignore[reportAttributeAccessIssue]
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild_id), text, "RARE")

        await ctx.respond(embed=reply)

    """Change the Starboard Shiny Catch Text"""

    @starboard_group.command(name="shiny-text", description="Customize the Shiny Catch Text")
    async def set_shiny_text(self, ctx: ApplicationContext, text: Option(str, description="Text", required=False, default=None)):
        if ctx.guild is None:
            return

        if not ctx.author.guild_permissions.administrator:  # pyright: ignore[reportAttributeAccessIssue]
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), "DEFAULT", "SHINY")
        else:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild_id), text, "SHINY")

        await ctx.respond(embed=reply)

    """Change the Starboard Rare Catch Image"""

    @starboard_group.command(name="rare-image", description="Customize the Rare Catch Image")
    async def set_rare_image(self, ctx: ApplicationContext, text: Option(str, description="Image Link", required=False, default=None)):
        if ctx.guild is None:
            return

        if not ctx.author.guild_permissions.administrator:  # pyright: ignore[reportAttributeAccessIssue]
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild_id), text, "RARE")

        await ctx.respond(embed=reply)

    """Change the Starboard Shiny Catch Image"""

    @starboard_group.command(name="shiny-image", description="Customize the Shiny Catch Image")
    async def set_shiny_image(self, ctx: ApplicationContext, text: Option(str, description="Image Link", required=False, default=None)):
        if ctx.guild is None:
            return

        if not ctx.author.guild_permissions.administrator:  # pyright: ignore[reportAttributeAccessIssue]
            return ctx.respond("Be an admin when :/")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "SHINY")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild_id), text, "SHINY")

        await ctx.respond(embed=reply)

    """ Send Sample Message in Starboard Channel """

    @starboard_group.command(name="send-sample", description="Sends a sample message in the starboard channel to check if the permissions are alright!")
    async def send_sample(self, ctx: ApplicationContext):
        if ctx.guild is None:
            return

        channel_id: str | None = await starboard_helper.get_starboard_channel_id(ctx.guild.id)
        if channel_id is None:
            logger.error("Can't send sample message because not channel id")
            return

        starboard_channel = await general_helper.get_channel_from_bot(ctx.bot, int(channel_id))

        if starboard_channel is None:
            return await ctx.respond(f"Can not find a channel with ID : {channel_id}. Try resetting the channel!")

        if not isinstance(starboard_channel, TextChannel):
            return await ctx.respond(f"Can only assign Text Channels not {starboard_channel.type}")  # pyright: ignore[reportAttributeAccessIssue]

        if not starboard_channel.permissions_for(ctx.guild.me).send_messages:
            return await ctx.respond("No Permission to send messages!")

        try:
            await starboard_channel.send("Sample Message! This channel is good for receiving starboard logs.")

        except Forbidden:
            await ctx.respond("Can't send messages to that channel, No Access")

        except Exception as e:  # noqa: BLE001
            ref_num = random.getrandbits(64)
            logger.error(f"Unable to send message to the channel : {starboard_channel.mention}, \n\terror : {e} reference number : {ref_num}")
            await ctx.respond(f"** SOME PROBLEM OCCURRED!**\nReport this at support server!\n`REFERENCE ID : {ref_num}`")


def setup(bot: commands.Bot):
    bot.add_cog(StarboardSlash())
