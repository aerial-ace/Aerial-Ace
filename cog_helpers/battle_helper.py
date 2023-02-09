from collections import OrderedDict
import discord

from managers import mongo_manager
from cog_helpers import general_helper
import config

# sends an confirmation message to accept the battle log
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
    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_data = data_cursor[0]["logs"]
        users = list(battle_data.keys())

        if winner not in users:
            battle_data[winner] = "1 | 0"
        else:
            try:
                wins  = int(battle_data[winner].split(" | ")[0]) + 1
                loses = battle_data[winner].split(" | ")[1]
            except:
                diff  = int(battle_data[winner])
                wins  = (1 if diff < 0 else diff + 1)
                loses = (0 if diff > 0 else abs(diff))

            battle_data[winner] = f"{wins} | {loses}"

        if loser not in users:
            battle_data[loser] = "0 | 1"
        else:
            try:
                wins  = int(battle_data[loser].split(" | ")[0])
                loses = int(battle_data[loser].split(" | ")[1]) + 1
            except:
                diff  = int(battle_data[loser])
                wins  = (0 if diff < 0 else diff)
                loses = (1 if diff > 0 else abs(diff) + 1)

            battle_data[loser] = f"{wins} | {loses}"

        updated_data = {"logs" : battle_data}

        await mongo_manager.manager.update_all_data("battles", query, updated_data)

        return f"> GG, <@{winner}> won over <@{loser}>. Scoreboard was updated."

    except Exception as e:
        print(f"Error while logging battle : {e}")
        return "Error occurred while logging battle!"

async def toggle_auto_logging(server_id:str):
    
    query = {"server_id" : server_id}
    data_cursor = await mongo_manager.manager.get_all_data("servers", query)

    try:
        auto_logging  = data_cursor[0].get("auto_battle_logging", 1)

        auto_logging = 1 if auto_logging == 0 else 0

        updated_data = {
            "auto_battle_logging" : auto_logging
        }

        await mongo_manager.manager.update_all_data("servers", query, updated_data)

    except:
        print("Error occurred while toggling Auto Battle Logging!")
        return "Error Occurred while toggling Auto Battle Logging!"

    else:
        return "Auto Battle Logging Module is now **{}**".format("Enabled" if auto_logging == 1 else "Disabled")

# return the battle score of the user
async def get_battle_score(server_id : int, user) -> discord.Embed:
    user_id = str(user.id)
    server_id = str(server_id)

    query = {"server_id" : server_id}
    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_data = data_cursor[0]["logs"]
        users = (battle_data.keys())

        if user_id not in users:
            return await general_helper.get_info_embd("Hold It", "> No registered battles were found.", config.WARNING_COLOR, "Register some battles first using lb command")
        else:
            wins  = int(battle_data[user_id].split(" | ")[0])
            loses = int(battle_data[user_id].split(" | ")[1])
            return await general_helper.get_info_embd(f"{user.name}'s Battle Score", f"_**Overall Diff**_  : **{wins - loses}**\n\n" + f"> _WINS_ : **{wins}**\n" + f"> _LOSES_ : **{loses}**", config.NORMAL_COLOR)

    except Exception as e:
        print(f"Error while showing battle score : {e}")
        return await general_helper.get_info_embd("Error!", "Error showing battle score :(, error were registered though.", config.ERROR_COLOR)

# returns the battle leaderboard of the server
async def get_battle_leaderboard_embed(guild):
    server_id = str(guild.id)
    server_name = guild.name

    query = {"server_id" : server_id}
    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_records:dict = data_cursor[0]["logs"]

        battle_records_diffs = {}
        for item in battle_records.items():
            try:
                battle_records_diffs[item[0]] = int(item[1].split(" | ")[0]) - int(item[1].split(" | ")[1])
            except:
                battle_records_diffs[item[0]] = item[1]

        sorted_battle_records = OrderedDict(sorted(battle_records_diffs.items(), key=lambda x: int(x[1]), reverse=True))

        reply_embd = discord.Embed(title="{server_name}'s battle leaderboard".format(server_name=server_name), color=discord.Color.blue())
        reply_embd.description = "`-N-  | -W- | -L- | -Win %- | -Name-` \n\n"

        max_leaderboard_listings = 20
        footer = ""

        pos = 1
        for i in sorted_battle_records:
            if pos > max_leaderboard_listings:
                footer = "Some players were not mentioned in the leaderboard because of lower scores.\nSee your score with -aa bs"
                break

            try:
                wins, loses  = [int(x) for x in battle_records[i].split(" | ")]
            except:
                value = int(battle_records[i])
                wins  = (0 if value < 0 else value)
                loses = (0 if value > 0 else abs(value))

            win_perc = (round((wins / (wins + loses)) * 100, 1) if wins + loses > 0 else 0)
                
            reply_embd.description += "`{pos} | {wins} | {loses} | {perc}% |` <@{id}> \n".format(pos=" {0}.".format(pos).center(4, " "), id=i, wins=("{0}".format(wins).center(3, " ")), loses=("{}".format(loses).center(3, " ")), perc=("{}".format(win_perc).rjust(6, " ")))
            pos = pos + 1

        if footer != "":
            reply_embd.set_footer(text=footer)

        return reply_embd
    except Exception as e:
        print(f"Error while showing battle leaderboard : {e}")
        return await general_helper.get_info_embd("Oops", "Error occurred while showing battle leaderboard :|", config.ERROR_COLOR, "These errors were registered")

# removes the user from the leaderboard
async def remove_user_from_battleboard(server_id : int, user : discord.Member):
    server_id = str(server_id)
    user_id = str(user.id)

    query = {"server_id" : server_id}

    mongo_cursor = await mongo_manager.manager.get_all_data("battles", query)

    battle_data = mongo_cursor[0]["logs"]

    users = list(battle_data.keys())

    if user_id in users:
        del(battle_data[user_id])
    else:
        return "> That user is not in the leaderboard"

    updated_data = {"logs" : battle_data}

    await mongo_manager.manager.update_all_data("battles", query, updated_data)

    return f"> <@{user_id}> was removed from the battle board."

# removes the user from the leaderboard
async def remove_user_from_battleboard_id(server_id : int, user_id:str):
    server_id = str(server_id)
    user_id = str(user_id)

    query = {"server_id" : server_id}

    mongo_cursor = await mongo_manager.manager.get_all_data("battles", query)

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

    await mongo_manager.manager.update_all_data("battles", query, updated_data)

    return f"> <@{user_id}> was removed from the battle board."

# clears the battle leaderboard of the server
async def clear_battleboard(server_id : str):

    try:
        query = {"server_id" : server_id}

        updated_data = {"logs" : {}}

        cursor = await mongo_manager.manager.update_all_data("battles", query, updated_data)
    except Exception as e:
        return f"Error happened while performing this command ```{e}```"
    else:
        return "Battle board cleared successfully."
