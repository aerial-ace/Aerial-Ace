from discord import Embed

import config
from cog_helpers import general_helper

all_categories = ["dex", "random_misc", "info", "battle", "tag", "fun", "misc", "starboard"]

all_commands = {
    "dex" : [
        "```{prefix}dex <PokemonName>``` displays the dex entry of the pokemon.",
        "```{prefix}ability <AbilityName>``` displays the overview of the ability"
    ],
    "random_misc" : [
        "```{prefix}random_poke[rp]``` displays a random pokemon with **some** info about it.",
        "```{prefix}random_team[rand_team]``` displays a random team of duelish pokemons.",
        "```{prefix}random_matchup[rand_matchup]``` displays a random matchup of duelish pokemons",
        "```{prefix}random_type[rand_type]``` displays a random type for monotype battles"
    ],
    "info" : [
        "```{prefix}stats <PokemonName>``` displays the must have stats for dueling of the pokemon.",
        "```{prefix}moveset[ms] <PokemonName>``` displays the must have moveset for dueling of the pokemon.",
        "```{prefix}nature <PokemonName>``` displays the must have nature for dueling of the pokemon.",
        "```{prefix}weakness[weak] <PokemonName or type combination>``` displays the **type** weakness of the pokemon."
    ],
    "battle" : [
        "```{prefix}log_battle[lb] @winner @loser``` logs the battle.",
        "```{prefix}battle_score[bs]``` displays the current battle score of the user.",
        "```{prefix}battle_lb[blb]``` displays the battle leaderboard of the server.",
        "```{prefix}battle_remove[br] @user``` removes the user from the battle board (Admin Only)",
        "```{prefix}battle_remove_id[brid] <user_id>``` removes the user from the battle board (Admin Only)"
    ],
    "tag" : [
        "```{prefix}tag <tag>``` assigns the user to the tag provided.",
        "```{prefix}tag_ping[tp] <tag>``` pings the users assigned to the tag provided.",
        "```{prefix}tag_show[ts] <tag>``` displays the users assigned to the tag provided.",
        "```{prefix}afk <on/off>``` set the afk",
        "```{prefix}tag_remove @user``` removes the user from their tag (Admin Only).",
        "```{prefix}tag_remove_id[trid] <user_id>``` removes the user from their tag (Admin Only)."
    ],
    "fun" : [
        "```{prefix}hit @target```, ```{prefix}kill @target```, ```{prefix}pat @target```, ```{prefix}dance [@target]```, ```{prefix}tease @target``` \nNo explanation is needed for these ig :3"
    ],
    "misc" : [
        "```{prefix}roll <UpperLimit>``` rolls a die",
        "```{prefix}ping``` displays the current bot latency",
        "```{prefix}support_server[ss]``` displays the link for the support server",
        "```{prefix}vote``` displays the vote link for the bot",
        "```{prefix}invite``` displays the invite link for the bot"
    ],
    "starboard" : [
        "```{prefix}starboard #channel``` sends rare catch embeds to this channel",
        "```{prefix}starboard``` disables the module"
    ]
}

async def get_help_embed(ctx = None) -> Embed:

    prefix = (ctx.prefix if ctx is not None else "/")

    embd = Embed(title="__HELP - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"Send `{prefix}help <category>` where category can be one from these : "
    embd.add_field(
        name="Categories",
        value="\n\n\n".join(all_categories),
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd

async def get_category_help_embed(ctx, category) -> Embed:

    category = category.lower()

    prefix = (ctx.prefix if ctx is not None else "/")

    if category not in all_categories:
        reply = await general_helper.get_info_embd("Not Found Error!", f"This category was not found, do `{prefix}help` for all the categories", color=config.ERROR_COLOR)
        return reply

    cmds = all_commands[category]

    for i in range(0, len(cmds)):
        cmds[i] = cmds[i].format(prefix=prefix)

    embd = Embed(title=f"__{category.capitalize()} Help__", color=config.NORMAL_COLOR)
    embd.description = "All the commands in this category"
    embd.add_field(
        name="Commands : ",
        value="\n".join(cmds),
        inline=False
    )

    embd.set_thumbnail(url=config.AVATAR_LINK)

    return embd