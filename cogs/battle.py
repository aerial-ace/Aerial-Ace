from discord.ext import commands

from cog_helpers import general_helper
from cog_helpers import battle_helper

class BattleSystem(commands.Cog):

    """Commands related to battling"""

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="log_battle", aliases=["lb"])
    async def log_battle(self, ctx, winner, loser):
        winner_id = await general_helper.get_user_id_from_ping(winner)
        loser_id = await general_helper.get_user_id_from_ping(loser)

        info = await battle_helper.get_battle_acceptance(self.bot, ctx, winner_id, loser_id)

        if info == "accepted":
            reply = await battle_helper.register_battle_log(ctx.guild.id, winner_id, loser_id)
        elif info == "notaccepted":
            reply = "> Battle log wasn't accepted."
        elif info == "error":
            reply = f"> Error occured while logging battles :/"
        else:
            return

        await ctx.send(reply)


def setup(bot):
    bot.add_cog(BattleSystem(bot))