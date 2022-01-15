import discord
from collections import OrderedDict

from bot import mongo_manager
from bot import aerialace
from bot import global_vars

# Register Battle log
async def register_battle_log(server_id, winner, looser):

    query = {"server_id" : server_id}
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

        if looser not in users:
            battle_data[looser] = -1
        else:
            battle_data[looser] = battle_data[looser] - 1

        updated_data = {"logs" : battle_data}

        mongo_manager.manager.update_all_data("battles", query, updated_data)

        return f"> GG, <@{winner}> won over <@{looser}>. Scoreboard was updated."

    except Exception as e:
        print(f"Error while logging battle : {e}")

# return the battle score of the user
async def get_battle_score(server_id, user):
    user_id = str(user.id)

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
            return "> Register some battles first -_-"
        else:
            score = battle_data[user_id]
            return f"> {user.name} has a battle score of **{score}**"

    except Exception as e:
        print(f"Error while showing battle score : {e}")
        return "> Error showing battle score :(, error were registered though."

# returns the battle leaderboard of the server
async def get_battle_leaderboard_embed(client, guild):
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

            player_name = f"<@{i}>"
            # TODO : Remove this user from leaderboards
            
            reply_embd.description += "`{pos} | {score} |` {name} \n".format(pos=" {0}.".format(pos).ljust(5, " "), name=("{0}".format(player_name)).ljust(20, " "), score=("{0}".format(battle_records[i]).ljust(7, " ")))
            pos = pos + 1

        if footer != "":
            reply_embd.set_footer(text=footer)

        return reply_embd
    except Exception as e:
        print(f"Error while showing battle leaderboard : {e}")
        return await aerialace.get_info_embd("Oops", "Error occured while showing battle leaderboards :|", global_vars.ERROR_COLOR, "These errors were registered")
