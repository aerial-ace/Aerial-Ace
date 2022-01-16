from managers import mongo_manager

async def get_battle_acceptance(bot, ctx, winner, loser):

    check_id = ""

    if winner == loser:
        await ctx.send("> Breh, Stop it")
        return "notapplicable"

    if str(ctx.author.id) == winner:
        check_id = loser
    elif str(ctx.author.id) == loser:
        check_id = winner
    else:
        await ctx.send("> Who are you to do this. Let the players log their battles.")
        return "notapplicable"

    # send battle log request
    log_msg = await ctx.send("Logging <@{winner}>'s win over <@{loser}>. Click the checkmark to accept.".format(winner=winner, loser=loser))

    accept_emoji = "☑️"

    await log_msg.add_reaction(accept_emoji)

    def check(_reaction, _user):
        print(_user.id)
        print(_reaction.emoji)
        return str(_user.id) == check_id and str(_reaction.emoji) == accept_emoji

    try:
        await bot.wait_for("reaction_add", timeout=10.0, check=check)
    except:
        return "notaccepted"
    else:
        return "accepted"

# Register Battle log
async def register_battle_log(server_id, winner, looser):

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

        if looser not in users:
            battle_data[looser] = -1
        else:
            battle_data[looser] = battle_data[looser] - 1

        updated_data = {"logs" : battle_data}

        mongo_manager.manager.update_all_data("battles", query, updated_data)

        return f"> GG, <@{winner}> won over <@{looser}>. Scoreboard was updated."

    except Exception as e:
        print(f"Error while logging battle : {e}")
        return "error"