from discord import Member
from discord.ext import commands

from cog_helpers import general_helper
from cog_helpers import battle_helper
import config

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

        await ctx.send(reply)

    @log_battle.error
    async def log_battle_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requries user pings as a parameter. Like this :```{ctx.prefix}lb @Wumpus @Dumpus```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

    """View Battleboard"""

    @commands.guild_only()
    @commands.command(name="battle_lb", aliases=["blb"])
    async def battle_lb(self, ctx):
        reply = await battle_helper.get_battle_leaderboard_embed(ctx.guild)
        await ctx.send(embed=reply)

    @battle_lb.error
    async def battle_lb_handler(self, ctx, error):
        await ctx.send(error)

    """View Battle Score"""

    @commands.guild_only()
    @commands.command(name="battle_score", aliases=["bs"])
    async def battle_score(self, ctx, user : Member = None):
        if user is None:
            reply = await battle_helper.get_battle_score(ctx.guild.id, ctx.author)
            await ctx.send(reply)
        else:
            reply = await battle_helper.get_battle_score(ctx.guild.id, user)
            await ctx.send(reply)

    @battle_score.error
    async def battle_score_handler(self, ctx, error):
        await ctx.send(error)

    """Remove user from battle leaderboard"""

    @commands.guild_only()
    @commands.command(name="battle_remove", aliases=["br"])
    async def battle_remove(self, ctx, user : Member):
        reply = await battle_helper.remove_user_from_battleboard(ctx.guild.id, user)
        await ctx.send(reply)

    @battle_remove.error
    async def battle_remove_handler(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            reply = await general_helper.get_info_embd("Breh, Whats this?", f"This command requires user_id as a parameter. Like this```{ctx.prefix}br 716390085896962058```", color=config.ERROR_COLOR)
            await ctx.reply(embed=reply)
        else:
            await ctx.send(error)

def setup(bot):
    bot.add_cog(BattleSystem(bot))