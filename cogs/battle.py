from discord import Member
from discord.ext import commands

from views.ButtonViews import GeneralView
from helpers import general_helper
from helpers import battle_helper
import config


class BattleSystem(commands.Cog):
    """Commands related to battling"""

    def __init__(self, bot):
        self.bot = bot

    """Log battles"""

    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name="log_battle", aliases=["lb"], description="Logs a battle in battle leaderboard")
    async def log_battle(self, ctx: commands.Context, winner: Member, loser: Member):

        info = await battle_helper.get_battle_acceptance(ctx, str(winner.id), str(loser.id))

        if info == "accepted":
            reply = await battle_helper.register_battle_log(ctx.guild.id, str(winner.id), str(loser.id), winner.name, loser.name)
        elif info == "notaccepted":
            reply = "> Battle log wasn't accepted."
            ctx.command.reset_cooldown(ctx)
        else:
            return

        view = GeneralView(200, True, True, False, True)

        await ctx.send(reply, view=view)

    @log_battle.error
    async def log_battle_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user pings as a parameter. Like this :```{ctx.prefix}lb @Wumpus @Dumpus```", color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.reply(embed=reply, view=view)

    """Toggle Auto Battle Logging"""

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.command(name="auto_battle_logging", aliases=["abl", "auto_bl"], description="Toggles Automatic Battle Logging")
    async def auto_battle_log(self, ctx: commands.Context):

        reply = await battle_helper.toggle_auto_logging(str(ctx.guild.id))

        await ctx.reply(reply)

    """View Battleboard"""

    @commands.guild_only()
    @commands.command(name="battle_lb", aliases=["blb"], description="Shows the battle leaderboard of the server")
    async def battle_lb(self, ctx):

        paginator = await battle_helper.get_battle_leaderboard_paginator(ctx.guild)

        await paginator.send(ctx)

    @battle_lb.error
    async def battle_lb_handler(self, ctx, error):
        await ctx.send(error)

    """View Battle Score"""

    @commands.guild_only()
    @commands.command(name="battle_score", aliases=["bs"], description="Returns the battle score the server member")
    async def battle_score(self, ctx, user: Member = None):
        if user is None:
            reply = await battle_helper.get_battle_score(ctx.guild.id, ctx.author)
            view = GeneralView(200, True, True, False, True)

            await ctx.send(embed=reply, view=view)
        else:
            reply = await battle_helper.get_battle_score(ctx.guild.id, user)
            view = GeneralView(200, True, True, False, True)

            await ctx.send(embed=reply, view=view)

    """Remove user from battle leaderboard"""

    @commands.guild_only()
    @commands.command(name="battle_remove", aliases=["br"],
                      description="Removes a server member from the battle leaderboard")
    @commands.has_permissions(administrator=True)
    async def battle_remove(self, ctx, user: Member):
        reply = await battle_helper.remove_user_from_battleboard(str(ctx.guild.id), user)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(reply, view=view)

    @battle_remove.error
    async def battle_remove_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?",
                                                       f"This command requires user as a parameter. Like this```{ctx.prefix}br @dumb_guy_69```",
                                                       color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.reply(reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Be an admin when :/")

    """Battle Remove using id"""

    @commands.guild_only()
    @commands.command(name="battle_remove_id", aliases=["brid"],
                      description="Removes a server member from the battle leaderboard using member id")
    @commands.has_permissions(administrator=True)
    async def battle_remove_id(self, ctx, user_id: str):
        reply = await battle_helper.remove_user_from_battleboard_id(str(ctx.guild.id), user_id)
        view = GeneralView(200, True, True, False, True)

        await ctx.send(reply, view=view)

    @battle_remove_id.error
    async def battle_remove_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?",
                                                       f"This command requires user_id as a parameter. Like this```{ctx.prefix}brid 716390085896962058```",
                                                       color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, True)

            await ctx.send(embed=reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Be an admin when :/")

    """Clear Battleboard at once"""

    @commands.guild_only()
    @commands.command(name="battleboard_clear", aliases=["blbc", "blb_clear"],
                      description="Clears the battle leaderboard of the server")
    @commands.has_permissions(administrator=True)
    async def battle_leaderboard_clear(self, ctx: commands.Context):
        reply = await battle_helper.clear_battleboard(str(ctx.guild.id))
        view = GeneralView(200, True, True, False, True)

        await ctx.send(reply, view=view)

    @battle_leaderboard_clear.error
    async def battle_leaderboard_clear_handler(self, ctx, error):
        await ctx.reply(error)


def setup(bot):
    bot.add_cog(BattleSystem(bot))
