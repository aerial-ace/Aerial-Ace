import random

from discord import Forbidden, TextChannel, Thread
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands

from helpers import starboard_helper
from managers.logging_manager import get_logger

logger = get_logger()


class StarboardSystem(commands.Cog):
    @commands.group(name="starboard", aliases=["sb"], description="A collection of commands to manage the starboard system in your server")
    async def starboard(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand!")

    """ Toggle Starboard Module / Set Channel """

    @starboard.command(name="channel", aliases=["ch"], description="Enables/Disables the starboard system with the provided channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx: commands.Context, channel: TextChannel | None = None):
        if ctx.guild is None:
            return await ctx.reply("Please use this command from server only!")

        reply = await starboard_helper.set_starboard(str(ctx.guild.id), channel)
        await ctx.reply(reply)

    """ Toggle High Res Images"""

    @starboard.command(name="highres", aliases=["hr"], description="Enables High Res images in starboard")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def toggle_highres(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.reply("Please use this command from a server only!")

        reply = await starboard_helper.set_highres(str(ctx.guild.id))

        await ctx.reply(reply)

    """ Set Alert Mask """

    @starboard.command(name="alertenable", aliases=["ae"], description="Enables alerts when a pokemon of this catch type is caught")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def enable_alerts(self, ctx: commands.Context, *, alerts: str):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        alerts_to_enable = alerts.lower().split()
        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]

        for alert in alerts_to_enable:
            if alert not in alert_types:
                return await ctx.reply("Not a valid alert type! Alert type can only be one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")

            reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert, True)

            await ctx.send(reply)

    """ Disable Alert Mask """

    @starboard.command(name="alertdisable", aliases=["ad"], description="Disables alerts when a pokemon of this catch type is caught")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable_alerts(self, ctx: commands.Context, *, alerts: str):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        alerts_to_disable = alerts.lower().split()
        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]

        for alert in alerts_to_disable:
            if alert not in alert_types:
                return await ctx.reply("Not a valid alert type! Alert type can only be one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")

            reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert, False)

            await ctx.send(reply)

    """ Information of Alert Mask """

    @starboard.command(name="alertinfo", aliases=["ai"], description="Gives Detailed info about which alerts are enabled.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def alert_info(self, ctx: commands.Context):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        reply = await starboard_helper.get_alert_info(str(ctx.guild.id))

        await ctx.send(embed=reply)

    """ Toggle / Set Shiny Starboard Channel """

    @starboard.command(name="shinychannel", aliases=["shch"], description="Enables/Disables the shiny starboard system with the provided channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_shiny_channel(self, ctx: commands.Context, channel: TextChannel | None = None):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        reply = await starboard_helper.set_shiny_starboard(str(ctx.guild.id), channel)

        await ctx.reply(reply)

    """Change the Starboard Catch Text"""

    @starboard.command(name="rare_text", aliases=["rt", "raretext"], description="Change the text shown for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_rare_text(self, ctx: commands.Context, text: str | None = None):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        if text is None:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), text, "RARE")

        await ctx.reply(embed=reply)

    """Change the Starboard Shiny Catch Text"""

    @starboard.command(name="shiny_text", aliases=["st", "shinytext"], description="Change the text shown for shiny catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_shiny_text(self, ctx: commands.Context, text: str = "DEFAULT"):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        if len(text) == 0:
            text = "DEFAULT"

        reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), text, "SHINY")

        await ctx.reply(embed=reply)

    """Change the Starboard Rare Catch Image"""

    @starboard.command(name="rare_image", aliases=["ri", "rareimage"], description="Change the Rare Catch Image for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_rare_image(self, ctx: commands.Context, text: str | None = None):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), text, "RARE")

        await ctx.reply(embed=reply)

    """Change the Starboard Shiny Catch Image"""

    @starboard.command(name="shiny_image", aliases=["si", "shinyimage"], description="Change the Shiny Catch Image for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_shiny_image(self, ctx: commands.Context, text: str | None = None):
        if ctx.guild is None:
            return await ctx.reply("Please this command from a server only!")

        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "SHINY")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), text, "SHINY")

        await ctx.reply(embed=reply)

    """Change Starboard Text"""

    @commands.command(name="")
    @starboard.error
    async def starboard_handler(self, ctx: commands.Context, error):
        if isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Be an Admin when :/")

    """Send Sample Message in starboard channel"""

    @starboard.command(name="sample", description="Sends a sample message in the assigned channel")
    async def send_sample(self, context: commands.Context):
        if context.guild is None:
            await context.reply("Please use this command in a server only!")
            return

        channel_id: str | None = await starboard_helper.get_starboard_channel_id(context.guild.id)
        if channel_id is None:
            await context.reply("Failed to recognize the starboard channel! \nTry setting the starboard channel again")
            return

        bt: commands.Bot = context.bot

        starboard_channel: GuildChannel | PrivateChannel | Thread | None = bt.get_channel(int(channel_id))

        if starboard_channel is None:
            return await context.send(f"Can not find a channel with ID : {channel_id}. Try resetting the channel!")

        if not isinstance(starboard_channel, TextChannel):
            return await context.send(f"Can only assign Text Channels not {starboard_channel.type}")  # pyright: ignore[reportAttributeAccessIssue]

        if not starboard_channel.permissions_for(context.guild.me).send_messages:
            return await context.send("No Permission to send messages!")

        try:
            await starboard_channel.send("Sample Message! This channel is good for receiving starboard logs.")

        except Forbidden:
            await context.reply(f"Failed to send message in {starboard_channel.mention}, not enough permissions!")

        except Exception as e:  # noqa: BLE001
            reference_number = random.getrandbits(64)
            logger.error(f"Failed to send sample message in {starboard_channel.mention}\n\terror : {e}")
            await context.reply(f"Failed to send message, Report to Support Server\n`REFERENCE NUMBER : {reference_number}`")


def setup(bot: commands.Bot):
    bot.add_cog(StarboardSystem())
