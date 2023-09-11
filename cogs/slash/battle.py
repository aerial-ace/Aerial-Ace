from discord import Member, ApplicationContext
from discord.ext import commands
from discord.commands import slash_command, Option

from helpers import battle_helper
from views.ButtonViews import GeneralView


class BattleSystemSlash(commands.Cog):
    """For viewing battleboard of the server"""

    bot: commands.Bot = None
    view: GeneralView = None

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.view = GeneralView(200, True, True, False, True)

    @slash_command(name="battle-leaderboard", description="View the battle leaderboard of this server")
    async def view_leaderboard(self, ctx: ApplicationContext):

        embd = await battle_helper.get_battle_leaderboard_paginator(ctx.guild)

        await ctx.respond(embed=embd, view=self.view)

    """For viewing the battle score"""

    @slash_command(name="battle-score", description="View the battle points of the user")
    async def view_score(self, ctx: ApplicationContext, user: Option(Member, description="View score of which user", required=False, default=None)):

        if user is None:
            user = ctx.author

        reply = await battle_helper.get_battle_score(ctx.guild.id, user)

        await ctx.respond(embed=reply, view=self.view)

    """Remove user from battle board"""

    @slash_command(name="battle-remove", description="Remove user from battle board")
    async def battle_remove(self, ctx: ApplicationContext, user: Option(Member, description="User to remove", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await battle_helper.remove_user_from_battleboard(str(ctx.guild.id), user)

        await ctx.respond(reply, view=self.view)

    """Remove user from battle board using user id"""

    @slash_command(name="battle-remove-id", description="Remove user from battle board using ids")
    async def battle_remove_id(self, ctx: ApplicationContext, user_id: Option(str, description="User to remove", required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Be Admin when? :/")

        reply = await battle_helper.remove_user_from_battleboard_id(str(ctx.guild.id), user_id)

        await ctx.respond(reply, view=self.view)

    """Clear Battle board at once"""

    @slash_command(name="battleboard-clear", description="Clears the complete battleboard of the server")
    async def clear_battleboard(self, ctx: ApplicationContext):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Admin Permissions are needed to run this command.")

        reply = await battle_helper.clear_battleboard(str(ctx.guild_id))

        await ctx.respond(reply, view=self.view)

    """Toggle AutoBattle Log module"""

    @slash_command(name="auto-battle-logging", description="Toggles the auto logging for battles on/off")
    async def toggle_abl(self, ctx: ApplicationContext):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond("Admin Permissions are needed to run this command.")

        reply = await battle_helper.toggle_auto_logging(str(ctx.guild.id))

        await ctx.respond(reply, view=self.view)


def setup(bot: commands.Bot):
    bot.add_cog(BattleSystemSlash(bot))
