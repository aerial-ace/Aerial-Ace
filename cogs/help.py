from ast import alias
import discord
from discord.ext import commands

import config
from cog_helpers import general_helper

all_categories = ["dex", "info", "battle", "tag", "misc"]

all_commands = {
    "dex" : [
        "`{prefix}dex <PokemonName>` displays the dex entry of the pokemon.",
        "`{prefix}random_poke[rp]` displays a random pokemon with **some** info about it.",
    ],
    "info" : [
        "`{prefix}stats <PokemonName>` displays the must have stats for dueling of the pokemon.",
        "`{prefix}moveset[ms] <PokemonName>` displays the must have moveset for dueling of the pokemon.",
        "`{prefix}nature <PokemonName>` displays the must have nature for dueling of the pokemon.",
        "`{prefix}weakness[weak] <PokemonName or type combination>` displays the **type** weakness of the pokemon."
    ],
    "battle" : [
        "`{prefix}log_battle[lb] @winner @loser` logs the battle.",
        "`{prefix}battle_score[bs]` displays the current battle score of the user.",
        "`{prefix}battle_lb[blb] displays the battle leaderboard of the server.`",
        "`{prefix}battle_remove[br] <User_id>` removes the user from the battle board (Admin Only)"
    ],
    "tag" : [
        "`{prefix}tag <tag>` assigns the user to the tag provided.",
        "`{prefix}tag_ping[tp] <tag>` pings the users assigned to the tag provided.",
        "`{prefix}tag_show[ts] <tag>` displays the users assigned to the tag provided.",
        "`{prefix}afk <on/off>` set the afk",
        "`{prefix}tag_remove <UserId>` removes the user from their tag (Admin Only)."
    ],
    "misc" : [
        "`{prefix}roll <UpperLimit>` rolls a die",
        "`{prefix}ping` displays the current bot latency",
        "`{prefix}support_server[ss]` displays the link for the support server",
        "`{prefix}vote` displays the vote link for the bot",
        "`{prefix}invite` displays the invite link for the bot"
    ]
}

all_admin_commands = [
    "`{prefix}mail_state <On/Off>` sets the mail reminder state. Turning it off will not remind users about mails",
    "`{prefix}show_date[sd] <Collection> <Server_ID>` shows the mondo db data of the server in the provided collection"
]

class HelpCommand(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.guild_only()
    @commands.command(name="help", aliases=["h"])
    async def send_help(self, ctx, category=None, command=None):

        if category is None:
            reply = await self.get_help_embed(ctx)
            await ctx.send(embed=reply)
            return

        if command is None:
            reply = await self.get_category_help_embed(ctx, category.lower())
            await ctx.send(embed=reply)
            return

    async def get_help_embed(self, ctx) -> discord.Embed:

        embd = discord.Embed(title="__HELP - Aerial Ace__", color=config.NORMAL_COLOR)
        embd.description = f"Send `{ctx.prefix}help <category>` where category can be one from these : "
        embd.add_field(
            name="Categories",
            value="\n".join(all_categories),
            inline=False
        )

        embd.set_thumbnail(url=config.AVATAR_LINK)

        return embd

    async def get_category_help_embed(self, ctx, category) -> discord.Embed:

        category = category.lower()

        if category not in all_categories:
            reply = await general_helper.get_info_embd("Not Found Error!", f"This category was not found, do `{ctx.prefix}help` for all the categories", color=config.ERROR_COLOR)
            return reply

        cmds = all_commands[category]

        for i in range(0, len(cmds)):
            cmds[i] = cmds[i].format(prefix=ctx.prefix)

        embd = discord.Embed(title=f"__{category.capitalize()} Help__", color=config.NORMAL_COLOR)
        embd.description = "All the commands in this category"
        embd.add_field(
            name="Commands : ",
            value="\n".join(cmds),
            inline=False
        )

        embd.set_thumbnail(url=config.AVATAR_LINK)

        return embd

    @commands.is_owner()
    @commands.command(name="admin_help", aliases=["ah"])
    async def send_admin_help(self, ctx):
        embd = discord.Embed(title="Admin Help Panel", color=config.NORMAL_COLOR)
        embd.description = "These commands can be used by bot owners only"

        cmds = "\n".join(all_admin_commands)

        for cmd in all_admin_commands:
            embd.add_field(
                name = "Commands : ",
                value=cmds,
                inline=False
            )

        await ctx.send(embd)

def setup(bot):
    bot.add_cog(HelpCommand(bot))