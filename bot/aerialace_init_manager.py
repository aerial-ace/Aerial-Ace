import discord
import json
import os

from bot import global_vars
from bot import aerialace_cache_manager

# register server in the database
async def register_guild(client, guild):
    server_id = str(guild.id)
    server_name = str(guild.name)

    # Load the data form the files
    fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
    fav_data = json.loads(fav_data_out.read())
    fav_data_out.close()

    server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
    server_data = json.loads(server_data_out.read())
    server_data_out.close()

    tag_data_out = open(global_vars.TAG_FILE_LOCATION, "r")
    tag_data = json.loads(tag_data_out.read())
    tag_data_out.close()

    battle_data_file = open(global_vars.BATTLE_LOG_FILE_LOCATION, "r")
    battle_data = json.loads(battle_data_file.read())
    battle_data_file.close()

    # update the data
    if server_id not in list(fav_data.keys()):
        fav_data[str(server_id)] = {}

    if server_id not in list(tag_data.keys()):
        tag_data[str(server_id)] = {}

    if server_id not in list(battle_data.keys()):
        battle_data[str(server_id)] = {}

    server_data[server_id] = server_name

    # Save the changes to the files
    fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
    json_obj = json.dumps(fav_data)
    fav_data_in.write(json_obj)
    fav_data_in.close()

    server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
    json_obj = json.dumps(server_data)
    server_data_in.write(json_obj)
    server_data_in.close()

    tag_data_in = open(global_vars.TAG_FILE_LOCATION, "w")
    json_obj = json.dumps(tag_data)
    tag_data_in.write(json_obj)
    tag_data_in.close()

    battle_data_in = open(global_vars.BATTLE_LOG_FILE_LOCATION, "w")
    json_obj = json.dumps(battle_data)
    battle_data_in.write(json_obj)
    battle_data_in.close()

    # cache the new data
    await aerialace_cache_manager.cache_data(init=False)

    # Dm the admins on server joins
    admin_id = int(os.environ['ADMIN_ID'])
    admin = client.get_user(admin_id)
    try:
        await admin.send("Aerial Ace was added to **{server}** :]".format(server=guild.name))
    except discord.Forbidden:
        print(
            "Unable to send message to admins. Btw, Aerial Ace was added to **{server}** :]".format(server=guild.name))

# remove server from the database
async def remove_guild(client, guild):
    server_id = str(guild.id)

    # Get the data from the files
    fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
    fav_data = json.loads(fav_data_out.read())
    fav_data_out.close()

    server_data_out = open(global_vars.SERVER_FILE_LOCATION, "r")
    server_data = json.loads(server_data_out.read())
    server_data_out.close()

    tag_data_out = open(global_vars.TAG_FILE_LOCATION, "r")
    tag_data = json.loads(tag_data_out.read())
    tag_data_out.close()

    battle_data_out = open(global_vars.BATTLE_LOG_FILE_LOCATION, "r")
    battle_data = json.loads(battle_data_out.read())
    battle_data_out.close()

    # update the data
    if server_id in list(fav_data.keys()):
        del fav_data[str(server_id)]

    if server_id in list(tag_data.keys()):
        del tag_data[str(server_id)]

    if server_id in list(server_data.keys()):
        del server_data[str(server_id)]

    if server_id in list(battle_data.keys()):
        del battle_data[str(server_id)]

    # Save the data to the files
    fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
    json_obj = json.dumps(fav_data)
    fav_data_in.write(json_obj)
    fav_data_in.close()

    server_data_in = open(global_vars.SERVER_FILE_LOCATION, "w")
    json_obj = json.dumps(server_data)
    server_data_in.write(json_obj)
    server_data_in.close()

    tag_data_in = open(global_vars.TAG_FILE_LOCATION, "w")
    json_obj = json.dumps(tag_data)
    tag_data_in.write(json_obj)
    tag_data_in.close()

    battle_data_in = open(global_vars.BATTLE_LOG_FILE_LOCATION, "w")
    json_obj = json.dumps(battle_data)
    battle_data_in.write(json_obj)
    battle_data_in.close()

    # cache the new data
    await aerialace_cache_manager.cache_data(init=False)

    # Dm the admins on server removal
    admin_id = int(os.environ['ADMIN_ID'])
    admin = client.get_user(admin_id)

    try:
        await admin.send("Aerial Ace was removed from **{server}** :_:".format(server=guild.name))
    except discord.Forbidden:
        print("Unable to send message to the admin. Btw, Aerial Ace was removed from {server} :_:".format(server=guild.name))
