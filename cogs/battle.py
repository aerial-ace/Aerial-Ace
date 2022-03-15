from discord import Member
from discord.ext import commands

import config
from cog_helpers import general_helper
from cog_helpers import battle_helper
from views.GeneralView import GeneralView

class BattleSystem(commands.Cog):

    """Commands related to battling"""

    def __init__(self, bot):
        self.bot = bot

    """Log battles"""

    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name="log_battle", aliases=["lb"])
    async def log_battle(self, ctx : commands.Context, winner, loser):
        winner_id = await general_helper.get_user_id_from_ping(winner)
        loser_id = await general_helper.get_user_id_from_ping(loser)

        info = await battle_helper.get_battle_acceptance(ctx, winner_id, loser_id)

        if info == "accepted":
            reply = await battle_helper.register_battle_log(ctx.guild.id, winner_id, loser_id)
        elif info == "notaccepted":
            reply = "> Battle log wasn't accepted."
            ctx.command.reset_cooldown(ctx)
        else:
            return

        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

    @log_battle.error
    async def log_battle_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requries user pings as a parameter. Like this :```{ctx.prefix}lb @Wumpus @Dumpus```", color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.reply(embed=reply, view=view)
        else:
            await ctx.send(error)

    """View Battleboard"""

    @commands.guild_only()
    @commands.command(name="battle_lb", aliases=["blb"])
    async def battle_lb(self, ctx):
        reply = await battle_helper.get_battle_leaderboard_embed(ctx.guild)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(embed=reply, view=view)

    @battle_lb.error
    async def battle_lb_handler(self, ctx, error):
        await ctx.send(error)

    """View Battle Score"""

    @commands.guild_only()
    @commands.command(name="battle_score", aliases=["bs"])
    async def battle_score(self, ctx, user : Member = None):
        if user is None:
            reply = await battle_helper.get_battle_score(ctx.guild.id, ctx.author)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(reply, view=view)
        else:
            reply = await battle_helper.get_battle_score(ctx.guild.id, user)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(reply, view=view)

    # @battle_score.error
    # async def battle_score_handler(self, ctx, error):
    #     await ctx.send(error)

    """Remove user from battle leaderboard"""

    @commands.guild_only()
    @commands.command(name="battle_remove", aliases=["br"])
    @commands.has_permissions(administrator=True)
    async def battle_remove(self, ctx, user : Member):
        reply = await battle_helper.remove_user_from_battleboard(ctx.guild.id, user)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(reply, view=view)

    @battle_remove.error
    async def battle_remove_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user as a parameter. Like this```{ctx.prefix}br @dumb_guy_69```", color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.reply(reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Be an admin when :/")
        else:
            await ctx.send(error)

    """Battle Remove using id"""

    @commands.guild_only()
    @commands.command(name="battle_remove_id", aliases=["brid"])
    @commands.has_permissions(administrator=True)
    async def battle_remove_id(self, ctx, user_id:str):
        reply = await battle_helper.remove_user_from_battleboard_id(ctx.guild.id, user_id)
        view = GeneralView(200, True, True, False, False)

        await ctx.send(reply, view=view)

    @battle_remove_id.error
    async def battle_remove_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user_id as a parameter. Like this```{ctx.prefix}brid 716390085896962058```", color=config.ERROR_COLOR)
            view = GeneralView(200, True, True, False, False)

            await ctx.send(embed=reply, view=view)
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.reply("Be an admin when :/")
        else:
            await ctx.send(error)

    """Clear Battleboard at once"""

    @commands.guild_only()
    @commands.command(name="battleboard_clear", aliases=["blbc", "blb_clear"])
    @commands.has_permissions(administrator=True)
    async def battle_leaderboard_clear(self, ctx:commands.Context):
        reply = await battle_helper.clear_battleboard(str(ctx.guild.id))
        view = GeneralView(200, True, True, False, False)

        await ctx.send(reply, view=view)

    @battle_leaderboard_clear.error
    async def battle_leaderboard_clear_handler(self, ctx, error):
        await ctx.reply(error)

def setup(bot):
    bot.add_cog(BattleSystem(bot))