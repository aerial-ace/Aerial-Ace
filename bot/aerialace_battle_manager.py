import discord
import json
from collections import OrderedDict

from bot import global_vars
from bot import aerialace_cache_manager

# Register Battle log
async def register_battle_log(server_id, winner, loser):
    # open the battle file
    battle_file_out = open(global_vars.BATTLE_LOG_FILE_LOCATION, "r")
    battle_data = json.loads(battle_file_out.read())
    battle_file_out.close()

    # get data from the battle file as {"user_id" : "wins"}
    battle_records = battle_data[str(server_id)]
    users = list(battle_records.keys())

    if winner in users:
        battle_data[server_id][winner] = str(int(battle_data[server_id][winner]) + 1)
    else:
        battle_data[server_id][winner] = "1"

    if loser in users:
        battle_data[server_id][loser] = str(int(battle_data[server_id][loser]) - 1)
    else:
        battle_data[server_id][loser] = "-1"

    # write the data
    battle_file_in = open(global_vars.BATTLE_LOG_FILE_LOCATION, "w")
    json_obj = json.dumps(battle_data)
    battle_file_in.write(json_obj)
    battle_file_in.close()

    # cache the data
    await aerialace_cache_manager.cache_data(init=False)

    return "> <@{0}> won over <@{1}>. Scoreboard was updated".format(winner, loser)


# return the battle score of the user
async def get_battle_score(server_id, user):
    cached_battle_data = aerialace_cache_manager.cached_battle_data

    user_id = str(user.id)

    if server_id not in list(cached_battle_data.keys()):
        return "> Server was not found in database, dm your server id to DevGa.me#0176 please"

    users = cached_battle_data[server_id]

    if user_id in users:
        score = cached_battle_data[server_id][user_id]
        return "> {user} has a battle score of **{score}**".format(user=user.name, score=score)
    else:
        return "> Register some battles first -_-"


# returns the battle leaderboard of the server
async def get_battle_leaderboard_embed(client, guild):
    cached_battle_data = aerialace_cache_manager.cached_battle_data

    server_id = str(guild.id)
    server_name = guild.name

    # {"user" : "wins"}
    battle_records = cached_battle_data[server_id]

    sorted_battle_records = OrderedDict(sorted(battle_records.items(), key=lambda x: int(x[1]), reverse=True))

    reply_embd = discord.Embed(title="{server_name}'s battle leaderboard".format(server_name=server_name), colour=discord.Colour.blue())
    reply_embd.description = "```-Pos- | --------Name-------- | --Score-- \n\n"

    max_leaderboard_listings = 10
    footer = ""

    pos = 1
    for i in sorted_battle_records:
        if pos > max_leaderboard_listings:
            footer = "Some players were not mentioned in the leaderboard because of lower scores.\nSee your score with -aa bs"
            break
        try:
            player_name = client.get_user(int(i)).name
        except:
            player_name = "Not Found"
        reply_embd.description += "{pos} | {name} | {score} \n".format(pos=" {0}.".format(pos).ljust(5, " "), name=("{0}".format(player_name)).ljust(20, " "), score=("{0}".format(battle_records[i]).ljust(9, " ")))
        pos = pos + 1

    reply_embd.description += "```"
    if footer != "":
        reply_embd.set_footer(text=footer)

    return reply_embd
