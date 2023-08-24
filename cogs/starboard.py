from discord.ext import commands
from discord import TextChannel

from helpers import starboard_helper


class StarboardSystem(commands.Cog):

    @commands.group(name="starboard", aliases=["sb"], description="A collection of commands to manage the starboard system in your server")
    async def starboard(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            await ctx.reply("Please provide a valid subcommand!")

    """Toggle Starboard Module"""

    @starboard.command(name="channel", aliases=["ch"], description="Enables/Disables the starboard system with the provided channel")
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def set_channel(self, ctx: commands.Context, channel: TextChannel = None):
        reply = await starboard_helper.set_starboard(str(ctx.guild.id), channel)

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


def setup(bot: commands.Bot):
    bot.add_cog(StarboardSystem())
