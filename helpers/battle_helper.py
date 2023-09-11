from collections import OrderedDict
from discord import Member, Embed, Guild

from views.PaginatorViews import PageView
from managers import mongo_manager
from helpers import general_helper, logger
from config import NORMAL_COLOR, ERROR_COLOR


# sends a confirmation message to accept the battle log
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
    except TimeoutError:
        return "notaccepted"
    else:
        return "accepted"


# Register Battle log
async def register_battle_log(server_id, winner, loser, winner_name=None, loser_name=None):
    query = {"server_id": str(server_id)}

    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    winner_name = winner_name or winner
    loser_name = loser_name or loser

    try:
        battle_data = data_cursor[0]["logs"]

        winner_data = battle_data.get(winner, None)

        if winner_data is None:
            battle_data[winner] = {
                "wins": 1,
                "loses": 0,
                "name": winner_name
            }
        else:
            battle_data[winner] = {
                "wins": battle_data[winner].get("wins", 0) + 1,
                "loses": battle_data[winner].get("loses", 0),
                "name": winner_name
            }

        loser_data = battle_data.get(loser, None)

        if loser_data is None:
            battle_data[loser] = {
                "wins": 0,
                "loses": 1,
                "name": loser_name
            }
        else:
            battle_data[loser] = {
                "wins": battle_data[loser].get("wins", 0),
                "loses": battle_data[loser].get("loses", 0) + 1,
                "name": loser_name
            }

        updated_data = {"logs": battle_data}

        await mongo_manager.manager.update_all_data("battles", query, updated_data)

        return f"> GG, <@{winner}> won over <@{loser}>. Scoreboard was updated."

    except Exception as e:
        logger.Logger.log_error(e, "Error occurred while logging battle!")
        return "Error occurred while logging battle!"


# Toggle server level auto battle logging functionality
async def toggle_auto_logging(server_id: str):
    query = {"server_id": server_id}
    data_cursor = await mongo_manager.manager.get_all_data("servers", query)

    try:
        auto_logging = data_cursor[0].get("auto_battle_logging", 1)

        auto_logging = 1 if auto_logging == 0 else 0

        updated_data = {
            "auto_battle_logging": auto_logging
        }

        await mongo_manager.manager.update_all_data("servers", query, updated_data)

    except Exception as e:
        logger.Logger.log_error(e, "Error occurred while toggling Auto Battle Logging!")
        return "Error Occurred while toggling Auto Battle Logging!"

    else:
        return "Auto Battle Logging Module is now **{}**".format("Enabled" if auto_logging == 1 else "Disabled")


# return the battle score of the user
async def get_battle_score(server_id: int, user: Member) -> Embed:
    user_id = str(user.id)
    server_id = str(server_id)

    query = {"server_id": server_id}
    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_data = data_cursor[0]["logs"]

        player = battle_data.get(user_id, None)

        if player is None:
            return await general_helper.get_info_embd(f"No registered battles were found for {user.mention}")

        wins = player.get("wins", 0)
        loses = player.get("loses", 0)
        win_perc = round(wins / (wins + loses) * 100, 2)

        return await general_helper.get_info_embd(f"Battle Score - {user.name}", f"Wins : **{wins}**\n" + f"Loses : **{loses}**\n" + f"Win Perc : **{win_perc}**\n" + f"Overall Diff : **{wins - loses}**", NORMAL_COLOR)

    except Exception as e:
        logger.Logger.log_error(e, f"Error while showing battle score")
        return await general_helper.get_info_embd("Error!", "Error showing battle score :(, error were registered though.", ERROR_COLOR)


# returns the battle leaderboard of the server
async def get_battle_leaderboard_paginator(guild: Guild = None, id: str = None) -> PageView:

    # works with both Guild Object and Guild Id alone
    if guild is not None:
        query = {"server_id": str(guild.id)}
    else:
        query = {"server_id": str(id)}

    data_cursor = await mongo_manager.manager.get_all_data("battles", query)

    try:
        battle_records: dict = data_cursor[0]["logs"]

        battle_records_diffs = {}

        for item in battle_records.items():
            wins = item[1].get("wins", 0)
            loses = item[1].get("loses", 0)
            name = item[1].get("name", item[0])

            battle_records_diffs[item[0]] = [wins - loses, wins, loses, name]

        sorted_battle_records: dict = OrderedDict(sorted(battle_records_diffs.items(), key=lambda x: int(x[1][0]), reverse=True))

        server_name = guild.name if guild is not None else str(id)

        max_leaderboard_listings = 20

        embds:list[Embed] = []

        current_embd = Embed(title=f"Battle Leaderboard - {server_name}", color=NORMAL_COLOR)
        current_embd.description = "`-N-  | -W- | -L- | -Win %- | -Name-` \n\n"

        for index, item in enumerate(sorted_battle_records.items()):

            # after max number of listings are added, add the previous embed to embds and start a new page.
            if index > max_leaderboard_listings:

                embds.append(current_embd)

                current_embd = Embed(title=f"Battle Leaderboard - {server_name}", color=NORMAL_COLOR)
                current_embd.description = "`-N-  | -W- | -L- | -Win %- | -Name-` \n\n"

            # stop loop if all listings are done.
            if index >= len(sorted_battle_records.items()) - 1:

                break

            wins = item[1][1]
            loses = item[1][2]
            name = item[1][3][:15] + "..." if len(item[1][3]) > 10 else item[1][3]
            win_perc = (round((wins / (wins + loses)) * 100, 1) if wins + loses > 0 else 0)

            current_embd.description += "`{pos} | {wins} | {loses} | {perc}% |` [{name}](https://discord.com/users/{id})\n".format(pos=" {0}.".format(index+1).center(4, " "), name=name, id=item[0], wins=("{0}".format(wins).center(3, " ")), loses=("{}".format(loses).center(3, " ")), perc=("{}".format(win_perc).rjust(6, " ")))

        paginator:PageView = PageView(pages=embds, show_all_btns=True)

        return paginator

    except Exception as e:
        logger.Logger.log_error(e, f"Error while showing battle leaderboard")
        return await general_helper.get_info_embd("Oops", "Error occurred while showing battle leaderboard :|", ERROR_COLOR, "These errors were registered")


# removes the user from the leaderboard
async def remove_user_from_battleboard(server_id: str, user: Member):
    query = {"server_id": server_id}

    mongo_cursor = await mongo_manager.manager.get_all_data("battles", query)

    battle_data = mongo_cursor[0]["logs"]

    user_data = battle_data.get(str(user.id), None)

    if user_data is None:
        return "> That user is not in the leaderboard"

    del (battle_data[str(user.id)])

    updated_data = {"logs": battle_data}

    await mongo_manager.manager.update_all_data("battles", query, updated_data)

    return f"> <@{user.id}> was removed from the battle board."


# removes the user from the leaderboard
async def remove_user_from_battleboard_id(server_id: str, user_id: str):
    query = {"server_id": server_id}

    mongo_cursor = await mongo_manager.manager.get_all_data("battles", query)

    battle_data = mongo_cursor[0]["logs"]

    user_data = battle_data.get(str(user_id), None)

    if user_data is None:
        return "> That user is not in the leaderboard"

    del (battle_data[user_id])

    updated_data = {"logs": battle_data}

    await mongo_manager.manager.update_all_data("battles", query, updated_data)

    return f"> <@{user_id}> was removed from the battle board."


# clears the battle leaderboard of the server
async def clear_battleboard(server_id: str):
    try:
        query = {"server_id": server_id}

        updated_data = {"logs": {}}

        await mongo_manager.manager.update_all_data("battles", query, updated_data)

    except Exception as e:
        return f"Error happened while performing this command ```{e}```"
    else:
        return "Battle board cleared successfully."
