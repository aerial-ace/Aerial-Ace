from collections import OrderedDict
import discord

from managers import mongo_manager
from cog_helpers import general_helper
import config

async def get_battle_acceptance(ctx, winner_id, loser_id):

    check_id = ""

    if winner_id == loser_id:
        await ctx.send("> Breh, Stop it")
        return "notapplicable"

    if str(ctx.author.id) == winner_id:
        check_id = loser_id
    elif str(ctx.author.id) == loser_id:
        check_id = winner_id
    else:
        await ctx.send("> Who are you to do this. Let the players log their battles.")
        return "notapplicable"

    # send battle log request
    log_msg = await ctx.send("Logging <@{winner}>'s win over <@{loser}>. Click the checkmark to accept.".format(winner=winner_id, loser=loser_id))

    accept_emoji = "☑️"

    await log_msg.add_reaction(accept_emoji)

    def check(_reaction, _user):
        return str(_user.id) == check_id and str(_reaction.emoji) == accept_emoji

    try:
        await ctx.bot.wait_for("reaction_add", timeout=10.0, check=check)
    except:
        return "notaccepted"
    else:
        return "accepted"

# Register Battle log
async def register_battle_log(server_id, winner, loser):

    query = {"server_id" : str(server_id)}
    data_cursor = mongo_manager.manager.get_all_data("battles", query)

    """
    {
        "object_id" : 10000000,
        "server_id" : "1000000",
        "battles" : {
            "user_id" : wins
        }
    }
    """

    try:
        battle_data = data_cursor[0]["logs"]
        users = list(battle_data.keys())

        if winner not in users:
            battle_data[winner] = 1
        else:
            battle_data[winner] = battle_data[winner] + 1

        if loser not in users:
            battle_data[loser] = -1
        else:
            battle_data[loser] = battle_data[loser] - 1

        updated_data = {"logs" : battle_data}

        mongo_manager.manager.update_all_data("battles", query, updated_data)

        return f"> GG, <@{winner}> won over <@{loser}>. Scoreboard was updated."

    except Exception as e:
        print(f"Error while logging battle : {e}")
        return "error"

# return the battle score of the user
async def get_battle_score(server_id : int, user):
    user_id = str(user.id)
    server_id = str(server_id)

    query = {"server_id" : server_id}
    data_cursor = mongo_manager.manager.get_all_data("battles", query)

    """
    {
        "object_id" : 1000000,
        "server_id" : "100000",
        "logs" : {
            "user_id" : 10
        }
    }
    """

    try:
        battle_data = data_cursor[0]["logs"]
        users = (battle_data.keys())

        if user_id not in users:
            return "> No registered battles were found -_-"
        else:
            score = battle_data[user_id]
            return f"> **{user.name}** has a battle score of **{score}**"

    except Exception as e:
        print(f"Error while showing battle score : {e}")
        return "> Error showing battle score :(, error were registered though."

# returns the battle leaderboard of the server
async def get_battle_leaderboard_embed(guild):
    server_id = str(guild.id)
    server_name = guild.name

    query = {"server_id" : server_id}
    data_cursor = mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_records = data_cursor[0]["logs"]

        sorted_battle_records = OrderedDict(sorted(battle_records.items(), key=lambda x: int(x[1]), reverse=True))

        reply_embd = discord.Embed(title="{server_name}'s battle leaderboard".format(server_name=server_name), colour=discord.Colour.blue())
        reply_embd.description = "`-Pos- | -Score- | -Name-` \n\n"

        max_leaderboard_listings = 15
        footer = ""

        pos = 1
        for i in sorted_battle_records:
            if pos > max_leaderboard_listings:
                footer = "Some players were not mentioned in the leaderboard because of lower scores.\nSee your score with -aa bs"
                break

            reply_embd.description += "`{pos} | {score} |` <@{id}> \n".format(pos=" {0}.".format(pos).ljust(5, " "), id=i, score=("{0}".format(battle_records[i]).ljust(7, " ")))
            pos = pos + 1

        if footer != "":
            reply_embd.set_footer(text=footer)

        return reply_embd
    except Exception as e:
        print(f"Error while showing battle leaderboard : {e}")
        return await general_helper.get_info_embd("Oops", "Error occured while showing battle leaderboards :|", config.ERROR_COLOR, "These errors were registered")

# removes the user from the leaderboard
async def remove_user_from_battleboard(server_id : int, user):
    server_id = str(server_id)
    user_id = str(user.id)

    query = {"server_id" : server_id}

    mongo_cursor = mongo_manager.manager.get_all_data("battles", query)

    battle_data = mongo_cursor[0]["logs"]

    """
    {
        "server_id" : "1000000",
        "logs" : {
            "user_id" : wins
        }
    }
    """

    users = list(battle_data.keys())

    if user_id in users:
        del(battle_data[user_id])
    else:
        return "> That user is not in the leaderboard"

    updated_data = {"logs" : battle_data}

    mongo_manager.manager.update_all_data("battles", query, updated_data)

    return f"> <@{user_id}> was removed from the battle board."
