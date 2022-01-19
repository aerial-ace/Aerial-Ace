import discord
from discord.ext import commands

import config
from cog_helpers import general_helper

all_categories = ["dex", "info", "battle", "tag", "misc"]

all_commands = {
    "dex" : [
        "`>>dex <PokemonName>` displays the dex entry of the pokemon.",
        "`>>random_poke[rp]` displays a random pokemon with **some** info about it.",
    ],
    "info" : [
        "`>>stats <PokemonName>` displays the must have stats for dueling of the pokemon.",
        "`>>moveset[ms] <PokemonName>` displays the must have moveset for dueling of the pokemon.",
        "`>>nature <PokemonName>` displays the must have nature for dueling of the pokemon.",
        "`>>weakness[weak] <PokemonName or type combination>` displays the **type** weakness of the pokemon."
    ],
    "battle" : [
        "`>>log_battle[lb] @winner @loser` logs the battle.",
        "`>>battle_score[bs]` displays the current battle score of the user.",
        "`>>battle_lb[blb] displays the battle leaderboard of the server.`",
        "`>>battle_remove[br] <User_id>` removes the user from the battle board (Admin Only)"
    ],
    "tag" : [
        "`>>tag <tag>` assigns the user to the tag provided.",
        "`>>tag_ping[tp] <tag>` pings the users assigned to the tag provided.",
        "`>>tag_show[ts] <tag>` displays the users assigned to the tag provided.",
        "`>>afk <on/off>` set the afk",
        "`>>tag_remove <UserId>` removes the user from their tag (Admin Only)."
    ],
    "misc" : [
        "`>>roll <UpperLimit>` rolls a die",
        "`>>ping` displays the current bot latency",
        "`>>support_server[ss]` displays the link for the support server",
        "`>>vote` displays the vote link for the bot",
        "`>>invite` displays the invite link for the bot",
    ]
}

class HelpCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="help", aliases=["h"])
    async def help(self, ctx, category=None, command=None):

        if category is None:
            reply = await self.get_help_embed()
            await ctx.send(embed=reply)
            return

        if command is None:
            reply = await self.get_category_help_embed(category.lower())
            await ctx.send(embed=reply)
            return

    async def get_help_embed(self) -> discord.Embed:

        embd = discord.Embed(title="__HELP - Aerial Ace__", color=config.NORMAL_COLOR)
        embd.description = "Send `>>help <category>` where category can be one from these : "
        embd.add_field(
            name="Categories",
            value="\n".join(all_categories),
            inline=False
        )

        embd.set_thumbnail(url=config.AVATAR_LINK)

        return embd

    async def get_category_help_embed(self, category) -> discord.Embed:

        if category not in all_categories:
            reply = await general_helper.get_info_embd("Not Found Error!", "This category was not found, do `>>help` for all the categories", color=config.ERROR_COLOR)
            return reply

        cmds = all_commands[category]

        embd = discord.Embed(title=f"__{category.capitalize()} Help__", color=config.NORMAL_COLOR)
        embd.description = "All the commands in this category"
        embd.add_field(
            name="Commands",
            value="\n".join(cmds),
            inline=False
        )

        embd.set_thumbnail(url=config.AVATAR_LINK)

        return embd

def setup(bot):
    bot.add_cog(HelpCommand(bot))