import pdb
from discord.ext import commands
from discord import TextChannel

from helpers import starboard_helper


class StarboardSystem(commands.Cog):

    @commands.group(name="starboard", aliases=["sb"], description="A collection of commands to manage the starboard system in your server")
    async def starboard(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand!")

    """ Toggle Starboard Module / Set Channel """

    @starboard.command(name="channel", aliases=["ch"], description="Enables/Disables the starboard system with the provided channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx: commands.Context, channel: TextChannel = None):
        reply = await starboard_helper.set_starboard(str(ctx.guild.id), channel)

        await ctx.reply(reply)

    """ Toggle High Res Images"""
    @starboard.command(name="highres", aliases=["hr"], description="Enables High Res images in starboard")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def toggle_highres(self, ctx:commands.Context):
        
        reply = await starboard_helper.set_highres(str(ctx.guild.id))
        
        await ctx.reply(reply)

    """ Set Alert Mask """
    @starboard.command(name="alertenable", aliases=["ae"], description="Enables alerts when a pokemon of this catch type is caught")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def enable_alerts(self, ctx:commands.Context, alert_type:str = None):
        
        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]
        
        if alert_type not in alert_types:
            return await ctx.reply("Not a valid alert type! Alert type can only be one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")

        reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert_type, True)
        
        await ctx.send(reply)
        
    """ Disable Alert Mask """
    @starboard.command(name="alertdisable", aliases=["ad"], description="Disables alerts when a pokemon of this catch type is caught")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def disable_alerts(self, ctx:commands.Context, alert_type:str = None):
        
        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]
        
        if alert_type not in alert_types:
            return await ctx.reply("Not a valid alert type! Alert type can only be one from : [rare/ regional/ shiny/ hunt/ gmax/ streak]")

        reply = await starboard_helper.set_alerts(str(ctx.guild.id), alert_type, False)
        
        await ctx.send(reply)

    """ Information of Alert Mask """
    @starboard.command(name="alertinfo", aliases=["ai"], description="Gives Detailed info about which alerts are enabled.")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def alert_info(self, ctx:commands.Context):
        
        alert_types = ["rare", "regional", "shiny", "hunt", "gmax", "streak"]
        
        reply = await starboard_helper.get_alert_info(str(ctx.guild.id))
        
        await ctx.send(embed=reply)

    """ Toggle / Set Shiny Starboard Channel """
    @starboard.command(name="shinychannel", aliases=["shch"], description="Enables/Disables the shiny starboard system with the provided channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_shiny_channel(self, ctx: commands.Context, channel: TextChannel = None):
        reply = await starboard_helper.set_shiny_starboard(str(ctx.guild.id), channel)

        await ctx.reply(reply)

    """Change the Starboard Catch Text"""

    @starboard.command(name="rare_text", aliases=["rt", "raretext"], description="Change the text shown for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_rare_text(self, ctx: commands.Context, text: str = None):
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
        if len(text) == 0:
            text = "DEFAULT"

        reply = await starboard_helper.set_starboard_text(str(ctx.guild.id), text, "SHINY")

        await ctx.reply(embed=reply)

    """Change the Starboard Rare Catch Image"""

    @starboard.command(name="rare_image", aliases=["ri", "rareimage"], description="Change the Rare Catch Image for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_rare_image(self, ctx: commands.Context, text: str = None):
        if text is None:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), "DEFAULT", "RARE")
        else:
            reply = await starboard_helper.set_starboard_image(str(ctx.guild.id), text, "RARE")

        await ctx.reply(embed=reply)

    """Change the Starboard Shiny Catch Image"""

    @starboard.command(name="shiny_image", aliases=["si", "shinyimage"], description="Change the Shiny Catch Image for rare catch!")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_shiny_image(self, ctx: commands.Context, text: str = None):
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
    async def send_sample(self, context:commands.Context):

        channel_id = await starboard_helper.send_sample(context.guild.id)

        bt:commands.Bot = context.bot

        starboard_channel = bt.get_channel(int(channel_id))

        if starboard_channel is None:
            return await context.send(f"Can not find a channel with ID : {channel_id}. Try resetting the channel!")
        
        if not isinstance(starboard_channel, TextChannel):
            return await context.send(f"Can only assign Text Channels not {starboard_channel.type}")
        
        if not starboard_channel.permissions_for(context.guild.me).send_messages:
            return await context.send(f"No Permission to send messages!")

        try:
            await starboard_channel.send("Sample Message! This channel is good for receiving starboard logs.")
        except Exception as e:
            await starboard_channel.send(embed=f"** SOME PROBLEM OCCURRED!**\nReport this at support server!```{e}```")

def setup(bot: commands.Bot):
    bot.add_cog(StarboardSystem())
