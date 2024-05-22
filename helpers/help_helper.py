from discord import Embed
from discord.ext import commands
import datetime

from helpers import general_helper, logger
import config

all_categories = {"pokedex": "commands related to pokedex", "random": "commands related to random gen", "info": "commands related to information", "battle": "commands related to battleboard", "tags": "commands related to shinyhunts", "fun": "other fun commands", "misc": "commands that dont fit in other categories", "starboard": "commands related to starboard", "smogon": "commands related to showdown", "donation" : "Displays the current donation information and holds commands related to donation module", "spawnrate" : "Commands related to Spawn Rate Module"}

commands_in_category = {
    "pokedex": ["dex", "ability"],
    "random": ["random_pokemon", "random_team", "random_matchup", "random_type"],
    "info": ["stats", "moveset", "nature", "weak"],
    "battle": ["log_battle", "battle_score", "battle_lb", "battle_remove", "battle_remove_id", "battleboard_clear", "auto_battle_logging"],
    "tags": ["tag", "tag_ping", "tag_show", "afk", "tag_remove", "tag_remove_id", "alltags"],
    "fun": ["hit", "pat", "kill", "hug", "tease", "cry", "dance"],
    "starboard": ["starboard"],
    "misc": ["ping", "roll", "support", "vote", "invite", "mail", "all"],
    "smogon": ["smogon"],
    "dono" : ["dono_channel", "dono_log", "dono_staff", "dono_change", "dono_clear", "dono_remove"],
    "spawnrate" : ["spawnrate.channel", "spawnrate.activate", "spawnrate.deactivate", "spawnrate.count"]
}

all_commands = {
    "dex": "```{prefix}dex[d] <PokemonName>\n{prefix}dex ditto```\ndisplays the dex entry of the pokemon.",
    "ability": "```{prefix}ability[ab] <AbilityName>\n{prefix}ability trace```\ndisplays the overview of the ability",
    "random_pokemon": "```{prefix}random_poke[rp]```\ndisplays a random pokemon with **some** info about it.",
    "random_team": "```{prefix}random_team[rand_team] <tier>\n{prefix}rand_team mega```\ndisplays a random team of duelish pokemons.",
    "random_matchup": "```{prefix}random_matchup[rand_matchup] <tier>\n{prefix}rand_matchup rare```\ndisplays a random matchup of duelish pokemons",
    "random_type": "```{prefix}random_type[rand_type]```\ndisplays a random type for monotype battles",
    "stats": "```{prefix}stats <PokemonName>\n{prefix}stats moltres```\ndisplays the must have stats for dueling of the pokemon.",
    "moveset": "```{prefix}moveset[ms] <PokemonName>\n{prefix}ms suicune```\ndisplays the must have moveset for dueling of the pokemon.",
    "nature": "```{prefix}nature <PokemonName>\n{prefix}nature azelf```\ndisplays the must have nature for dueling of the pokemon.",
    "weak": "```{prefix}weakness[weak] <PokemonName or type combination>\n{prefix}weak kyurem\n{prefix}weak fire water grass```\ndisplays the **type** weakness of the pokemon.",
    "log_battle": "```{prefix}log_battle[lb] @winner @loser```\nlogs the battle with winner @winner and loser @loser",
    "battle_score": "```{prefix}battle_score[bs] <user(Optional)>\n{prefix}bs\n{prefix}bs @Wumpus```\ndisplays the current battle score of the user.",
    "battle_lb": "```{prefix}battle_lb[blb]```\ndisplays the battle leaderboard of the server.",
    "battle_remove": "```{prefix}battle_remove[br] @user\n{prefix}br @Wumpus```\nremoves the user from the battle board (Admin Only)",
    "battle_remove_id": "```{prefix}battle_remove_id[brid] <user_id>\n{prefix}brid 716390085896962058```\nremoves the user from the battle board (Admin Only)",
    "auto_battle_logging": "```{prefix}auto_battle_logging[abl, auto_bl]\n{prefix}abl```\nToggles Auto Battle Logging Module (Admin Only)",
    "tag": "```{prefix}tag <tag>\n{prefix}tag pawniard```\nassigns the user to the tag provided.",
    "tag_ping": "```{prefix}tag_ping[tp] <tag>\n{prefix}tp axew```\npings the users assigned to the tag provided.",
    "tag_show": "```{prefix}tag_show[ts] <tag>\n{prefix}ts basculin```\ndisplays the users assigned to the tag provided.",
    "afk": "```{prefix}afk <on/off>\n{prefix}afk on\n{prefix}afk off```\nset the afk",
    "tag_remove": "```{prefix}tag_remove[tr] @user\n{prefix}tr @Wumpus```\nremoves the user from their tag (Admin Only).",
    "tag_remove_id": "```{prefix}tag_remove_id[trid] <user_id>\n{prefix}trid 716390085896962058```\nremoves the user from their tag (Admin Only).",
    "hit": "```{prefix}hit @target```\nhit anyone using pokemon gifs",
    "kill": "```{prefix}kill @target```\nkill anyone using pokemon gifs",
    "pat": "```{prefix}pat @target```\npat anyone using pokemon gifs",
    "dance": "```{prefix}dance [@target]```\ndance solo or with anyone using pokemon gifs",
    "tease": "```{prefix}tease @target```\ntease anyone using pokemon gifs",
    "hug": "```{prefix}hug @target```\nhug anyone using pokemon gifs",
    "cry": "```{prefix}cry```\n cry using pokemon gifs",
    "roll": "```{prefix}roll <UpperLimit>\n{prefix}roll 69```\nrolls a die",
    "ping": "```{prefix}ping```\ndisplays the current bot latency",
    "support": "```{prefix}support_server[ss]```\ndisplays the link for the support server",
    "vote": "```{prefix}vote```\ndisplays the vote link for the bot",
    "invite": "```{prefix}invite```\ndisplays the invite link for the bot",
    "mail": "```{prefix}mail```\nopens up the mail box with latest news about the bot",
    "starboard": "```{prefix}starboard[sb] channel[ch] #channel\n{prefix}sb shinychannel[shch] #shiny-starboard\n{prefix}sb raretext[rt] <text>\n{prefix}sb shinytext[st] <text>\n{prefix}sb shinyimage[si] <image_url>\n{prefix}sb rareimage[ri] <image_url>\n{prefix}sb sample //sends a sample embed to test perms.```\nsends rare catch embeds to this channel",
    "smogon": "```DISCONTINUED```",
    "all": "```{prefix}all``` returns a list of all the commands in the bot",
    "spawnrate.channel": "```{prefix}spawnrate[sr] channel[ch] #channel```\nsets the provided channel for spwan speed display.",
    "spawnrate.activate": "```{prefix}spawnrate[sr] activate[a]```\nactivates the spawnrate display! Make sure to set the channel first.",
    "spawnrate.deactivate": "```{prefix}spawnrate[sr] deactivate[da]```\ndeactivates the spawnrate display!",
    "spawnrate.count": "```{prefix}spawnrate[sr] count[c]```\nthe current spawn rate of the server!"
}

""" DISPOSED DONATION COMMANDS 

"dono_lb": "```{prefix}dono lb``` shows the current donation leaderboard of the server",
"dono_channel": "```{prefix}dono ch #channel``` donations made only in the #channel will be counted for the leaderboard",
"dono_log": "```{prefix}dono log #channel``` all the donation logs are sent in the #channel",
"dono_staff": "```{prefix}dono staff <role-id>``` sets the <role-id> as the staff role id. Donations taken by the staff with this role will be counted in the leaderboard.",
"dono_change": "```{prefix}dono change @user <pc> <shiny> <rare> <redeem>``` updates the leaderboard for the @user and sets their pc, shiny, rare, redeem values to the provided values.",
"dono_clear": "```{prefix}dono clear``` clears the leaderboard.",
"dono_remove": "```{prefix}dono remove @user``` removes @user from the leaderboard.",

"""

async def get_help_embed(ctx=None) -> Embed:
    prefix = (ctx.prefix if ctx is not None else "/")

    embd = Embed(title="__HELP - Aerial Ace__", color=config.NORMAL_COLOR)
    embd.description = f"Send `{prefix}help <category>` where category can be one from these : "

    categories = list(all_categories.keys())
    desc = list(all_categories.values())

    for i in range(len(categories)):
        embd.add_field(
            name=categories[i],
            value=desc[i],
            inline=True
        )

    embd.set_thumbnail(url=config.AVATAR_LINK)
    embd.timestamp = datetime.datetime.now()

    return embd


async def get_category_help_embed(ctx: commands.Context | None, input) -> Embed:
    input = input.lower()

    prefix = (ctx.prefix if ctx is not None else "/")

    categories = list(all_categories.keys())
    commands = list(all_commands.keys())

    input_is_command = False

    if input not in commands:
        if input not in categories:
            reply = await general_helper.get_info_embd("Not Found Error!", f"This category/command was not found, do `{prefix}help` for all the categories", color=config.ERROR_COLOR)
            return reply
        else:
            input_is_command = False
    else:
        input_is_command = True

    if input_is_command:
        desc = all_commands[input]
        embd = Embed(title=f"__{input.capitalize()} Help__", color=config.NORMAL_COLOR)

        try:
            embd.description = desc.format(prefix=prefix)

        except Exception as e:
            logger.Logger.log_error(e)

        embd.timestamp = datetime.datetime.now()
    else:
        if ctx is not None:
            cmds = commands_in_category[input]

            embd = Embed(title=f"__{input.capitalize()} Help__", color=config.NORMAL_COLOR)
            embd.description = "All the commands in this category, Use aa.help <command> to know more"

            for i in cmds:
                try:
                    j = " ".join(i.split("."))
                    desc = ctx.bot.get_command(j).description
                except:
                    desc = i

                embd.add_field(
                    name=i,
                    value=desc,
                    inline=True
                )

            embd.set_thumbnail(url=config.AVATAR_LINK)
            embd.timestamp = datetime.datetime.now()
        else:
            reply = await general_helper.get_info_embd("Not Found Error!", f"This command was not found, do `{prefix}help` for all the categories", color=config.ERROR_COLOR)
            return reply

    return embd
