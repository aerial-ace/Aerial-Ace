from discord import Embed
from discord.ext import commands
import datetime

import config
from cog_helpers import general_helper

all_categories = {"pokedex" : "commands related to pokedex", "random" : "commands related to random gen", "info" : "commands related to information", "battle" : "commands related to battleboard", "tags" : "commands related to shinyhunts", "fun" : "other fun commands", "misc" : "commands that dont fit in other catagories", "starboard" : "commands related to starboard", "smogon" : "commands related to showdown"}

commands_in_catagory = {
    "pokedex" : ["dex", "ability"],
    "random" : ["random_pokemon", "random_team", "random_matchup", "random_type"],
    "info" : ["stats", "moveset", "nature", "weak"],
    "battle" : ["log_battle", "battle_score", "battle_lb", "battle_remove", "battle_remove_id", "battleboard_clear"],
    "tags" : ["tag", "tag_ping", "tag_show", "afk", "tag_remove", "tag_remove_id", "alltags"],
    "fun" : ["hit", "pat", "kill", "hug", "tease", "cry", "dance"],
    "starboard" : ["starboard"],
    "misc" : ["ping", "roll", "support", "vote", "invite", "mail", "all"],
    "smogon" : ["smogon"]
}

all_commands = {
    "dex" : "```{prefix}dex[d] <PokemonName>\n{prefix}dex ditto```\ndisplays the dex entry of the pokemon.",
    "ability" : "```{prefix}ability[ab] <AbilityName>\n{prefix}ability trace```\ndisplays the overview of the ability",
    "random_pokemon" : "```{prefix}random_poke[rp]```\ndisplays a random pokemon with **some** info about it.",
    "random_team" : "```{prefix}random_team[rand_team] <tier>\n{prefix}rand_team mega```\ndisplays a random team of duelish pokemons.",
    "random_matchup" : "```{prefix}random_matchup[rand_matchup] <tier>\n{prefix}rand_matchup rare```\ndisplays a random matchup of duelish pokemons",
    "random_type" : "```{prefix}random_type[rand_type]```\ndisplays a random type for monotype battles",
    "stats" : "```{prefix}stats <PokemonName>\n{prefix}stats moltres```\ndisplays the must have stats for dueling of the pokemon.",
    "moveset" : "```{prefix}moveset[ms] <PokemonName>\n{prefix}ms suicune```\ndisplays the must have moveset for dueling of the pokemon.",
    "nature" : "```{prefix}nature <PokemonName>\n{prefix}nature azelf```\ndisplays the must have nature for dueling of the pokemon.",
    "weak" : "```{prefix}weakness[weak] <PokemonName or type combination>\n{prefix}weak kyurem\n{prefix}weak fire water grass```\ndisplays the **type** weakness of the pokemon.",
    "log_battle" : "```{prefix}log_battle[lb] @winner @loser```\nlogs the battle with winner @winner and loser @loser",
    "battle_score" : "```{prefix}battle_score[bs] <user(Optional)>\n{prefix}bs\n{prefix}bs @Wumpus```\ndisplays the current battle score of the user.",
    "battle_lb" : "```{prefix}battle_lb[blb]```\ndisplays the battle leaderboard of the server.",
    "battle_remove" : "```{prefix}battle_remove[br] @user\n{prefix}br @Wumpus```\nremoves the user from the battle board (Admin Only)",
    "battle_remove_id" : "```{prefix}battle_remove_id[brid] <user_id>\n{prefix}brid 716390085896962058```\nremoves the user from the battle board (Admin Only)",
    "tag" : "```{prefix}tag <tag>\n{prefix}tag pawniard```\nassigns the user to the tag provided.",
    "tag_ping" : "```{prefix}tag_ping[tp] <tag>\n{prefix}tp axew```\npings the users assigned to the tag provided.",
    "tag_show" : "```{prefix}tag_show[ts] <tag>\n{prefix}ts basculin```\ndisplays the users assigned to the tag provided.",
    "afk" : "```{prefix}afk <on/off>\n{prefix}afk on\n{prefix}afk off```\nset the afk",
    "tag_remove" : "```{prefix}tag_remove[tr] @user\n{prefix}tr @Wumpus```\nremoves the user from their tag (Admin Only).",
    "tag_remove_id" : "```{prefix}tag_remove_id[trid] <user_id>\n{prefix}trid 716390085896962058```\nremoves the user from their tag (Admin Only).",
    "hit" : "```{prefix}hit @target```\nhit anyone using pokemon gifs",
    "kill" : "```{prefix}kill @target```\nkill anyone using pokemon gifs",
    "pat" : "```{prefix}pat @target```\npat anyone using pokemon gifs",
    "dance" : "```{prefix}dance [@target]```\ndance solo or with anyone using pokemon gifs",
    "tease" : "```{prefix}tease @target```\ntease anyone using pokemon gifs",
    "hug" : "```{prefix}hug @target```\nhug anyone using pokemon gifs",
    "cry" : "```{prefix}cry```\n cry using pokemon gifs",
    "roll" : "```{prefix}roll <UpperLimit>\n{prefix}roll 69```\nrolls a die",
    "ping" : "```{prefix}ping```\ndisplays the current bot latency",
    "support" : "```{prefix}support_server[ss]```\ndisplays the link for the support server",
    "vote" : "```{prefix}vote```\ndisplays the vote link for the bot",
    "invite" : "```{prefix}invite```\ndisplays the invite link for the bot",
    "mail" : "```{prefix}mail```\nopens up the mail box with latest news about the bot",
    "starboard" : "```{prefix}starboard[sb] #channel\n{prefix}sb #poketwo-starboard```\nsends rare catch embeds to this channel",
    "smogon" : "```{prefix}smogon <gen> <tier> <pokemon>\n{prefix}smogon 5 OU durant```\nreturns the detailed usage data of the pokemon from the smogon database",
    "all" : "```{prefix}all``` returns a list of all the commands in the bot"
}

async def get_help_embed(ctx = None) -> Embed:

    prefix = (ctx.prefix if ctx is not None else "/")

    embd = Embed(title="__HELP - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"Send `{prefix}help <catagory>` where catagory can be one from these : "

    catagories = list(all_categories.keys())
    desc = list(all_categories.values())

    for i in range(len(catagories)):
        embd.add_field(
            name=catagories[i],
            value=desc[i],
            inline=True
        )

    embd.set_thumbnail(url=config.AVATAR_LINK)
    embd.timestamp = datetime.datetime.now()

    return embd

async def get_catagory_help_embed(ctx:commands.Context, input) -> Embed:

    input = input.lower()

    prefix = (ctx.prefix if ctx is not None else "/")

    catagories = list(all_categories.keys())
    commands = list(all_commands.keys())

    input_is_command = False

    if input not in commands:
        if input not in catagories:
            reply = await general_helper.get_info_embd("Not Found Error!", f"This catagory/command was not found, do `{prefix}help` for all the categories", color=config.ERROR_COLOR)
            return reply
        else:
            input_is_command = False
    else:
        input_is_command = True

    if input_is_command:
        desc = all_commands[input]
        embd = Embed(title=f"__{input.capitalize()} Help__", color=config.NORMAL_COLOR)
        embd.description = desc.format(prefix=ctx.prefix)
        embd.timestamp = datetime.datetime.now()
    else:
        cmds = commands_in_catagory[input]   

        embd = Embed(title=f"__{input.capitalize()} Help__", color=config.NORMAL_COLOR)
        embd.description = "All the commands in this catagory, Use aa.help <command> to know more"
        
        for i in cmds:
            desc = ctx.bot.get_command(i).description
            embd.add_field(
                name=i,
                value=desc,
                inline=True
            )

        embd.set_thumbnail(url=config.AVATAR_LINK)
        embd.timestamp = datetime.datetime.now()

    return embd