import discord
import os
import json

from bot import aerialace
from bot import global_vars
from bot import aerialace_cache_manager
from bot import mongo_manager

# return data files
async def send_data_files(client):
    stats_file = discord.File(global_vars.STATS_FILE_LOCATION)
    fav_file = discord.File(global_vars.FAV_FILE_LOCATION)
    server_file = discord.File(global_vars.SERVER_FILE_LOCATION)
    tag_file = discord.File(global_vars.TAG_FILE_LOCATION)
    battle_log_file = discord.File(global_vars.BATTLE_LOG_FILE_LOCATION)

    data_files = [stats_file, fav_file, server_file, tag_file, battle_log_file]

    # DM the files to the admins
    admin_id = int(os.environ['ADMIN_ID'])
    admin = client.get_user(admin_id)
    try:
        for file in data_files:
            await admin.send(file=file)
    except discord.Forbidden:
        print("Unable to send message to admins.")

# Set the favourite pokemon of the user
async def set_fav(server_id, user_id, poke_name):
    if poke_name == "":
        return "> Breh, give a pokemon name as a parameter like ```-aa set_fav espurr```"

    # get the data from the file
    fav_data_out = open(global_vars.FAV_FILE_LOCATION, "r")
    fav_data = json.loads(fav_data_out.read())
    fav_data_out.close()

    # update the data
    fav_data[server_id][user_id] = poke_name

    # save the data
    fav_data_in = open(global_vars.FAV_FILE_LOCATION, "w")
    json_obj = json.dumps(fav_data)
    fav_data_in.write(json_obj)
    fav_data_in.close()

    # update the cached data
    await aerialace_cache_manager.cache_data(init=False)

    return "> Your favourite pokemon is now **{fav}**. Check it using ```-aa fav```".format(fav=poke_name)

# Get the favourite pokemon of the user
async def get_fav(server_id, user_id):
    cached_fav_data = aerialace_cache_manager.cached_fav_data

    server_list = list(cached_fav_data.keys())  # all the registered servers

    if server_id in server_list:
        users = list(cached_fav_data[server_id].keys())
        if user_id in users:
            fav_poke = cached_fav_data[server_id][user_id]
            return "> Your favourite pokemon is **{}**".format(fav_poke.capitalize())
        else:
            return "> User was not found in the database, set you favourite using ```-aa set_fav <pokemon>```"
    else:
        return "> Server was not found! Dm DevGa.me#0176 smh"

# get duelish stats
async def get_stats_embed(pokemon):

    if pokemon == "":
        return aerialace.get_info_embd("Gib pokemon name as a param when :/", "A pokemon name is required for this command. Try this ```-aa stats Solgaleo```", global_vars.ERROR_COLOR)

    embd = discord.Embed()

    cached_stats_data = aerialace_cache_manager.cached_stats_data

    all_pokemon = list(cached_stats_data.keys())
    embd.colour = global_vars.NORMAL_COLOR

    if pokemon in all_pokemon:
        embd.title = "{poke}'s Stats".format(poke=pokemon.capitalize())
        embd.description = "HP, Defense, Sp.Defense and Speed are `The more the better` stats \n"
        embd.add_field(name="Stats", value="{stats}".format(stats=cached_stats_data[pokemon]), inline=False)

        return embd

    else:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"
        return embd

# get moveset
async def get_moveset_embed(poke):

    if poke == "":
        return aerialace.get_info_embd("Gib pokemon name as a param when :/", "A pokemon name is required for this command, try this ```-aa moveset Zekrom```", global_vars.ERROR_COLOR)

    embd = discord.Embed()

    cached_moveset_data = aerialace_cache_manager.cached_moveset_data

    all_pokemon = list(cached_moveset_data.keys())
    embd.colour = global_vars.NORMAL_COLOR

    if poke in all_pokemon:
        embd.title = "{poke}'s moveset".format(poke=poke.capitalize())
        embd.description = "{ms}".format(ms=cached_moveset_data[poke])
        return embd
    else:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"
        return embd

# return tierlist
async def get_tl(list_name):
    if list_name == "rare":
        return global_vars.RARE_TL
    elif list_name == "mega":
        return global_vars.MEGA_TL
    elif list_name == "common":
        return global_vars.COMMON_TL
    elif list_name == "normal":
        return global_vars.NORMAL_TL
    elif list_name == "fire":
        return global_vars.FIRE_TL
    elif list_name == "water":
        return global_vars.WATER_TL
    elif list_name == "grass":
        return global_vars.GRASS_TL
    elif list_name == "electric":
        return global_vars.ELECTRIC_TL
    elif list_name == "psychic":
        return global_vars.PSYCHIC_TL
    elif list_name == "rock":
        return global_vars.ROCK_TL
    elif list_name == "ground":
        return global_vars.GROUND_TL
    elif list_name == "fighting":
        return global_vars.FIGHTING_TL
    elif list_name == "ghost":
        return global_vars.GHOST_TL
    elif list_name == "dark":
        return global_vars.DARK_TL
    elif list_name == "ice":
        return global_vars.ICE_TL
    elif list_name == "fairy":
        return global_vars.FAIRY_TL
    elif list_name == "dragon":
        return global_vars.DRAGON_TL
    elif list_name == "steel":
        return global_vars.STEEL_TL
    elif list_name == "flying":
        return global_vars.FLYING_TL
    elif list_name == "poison":
        return global_vars.POISON_TL
    elif list_name == "bug":
        return global_vars.BUG_TL
    else:
        return """> That tierlist was not found, these tierlists are available```common | mega | fire```"""

# register shiny tags
async def register_tag(server_id, user_id, user_nick, tag):

    if tag == "":
        return "> Gib a tag name when? Like this ```-aa tag Ralts```"

    query = {"server_id" : server_id}

    """
    Structure : 
    {
        object_id : "10000000000000",
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_id" : ["user_id_1", "user_id_2"]
        }
    }
    """

    server_document = mongo_manager.manager.get_all_data("tags", query)

    details = server_document[0]

    tag_data = details["tags"]
    tags = list(tag_data.keys())
    users = list(tag_data.values())

    old_tag = ""

    for i in range(0, len(users)):
        if user_id in users[i]:
            old_tag = tags[i]
            break

    if old_tag == tag:
        return f"> **{user_nick}** is already assigned to `{tag.capitalize()}` tag"

    if old_tag != "":
        # remove user from current tag
        tag_data[old_tag].remove(user_id)

        # remove empty tags
        if len(tag_data[old_tag]) <= 0:
            del tag_data[old_tag]

    try:
        users_assigned_to_new_tag = tag_data[tag]
    except:
        tag_data[tag] = []
        users_assigned_to_new_tag = []

    users_assigned_to_new_tag.append(user_id)

    tag_data[tag] = users_assigned_to_new_tag 

    updated_data = {"tags" : tag_data}

    mongo_manager.manager.update_all_data("tags", {"server_id" : server_id}, updated_data)

    if old_tag == "":
        return f"> **{user_nick}** was assigned to `{tag.capitalize()}` tag"
    else:
        return f"> **{user_nick}** was removed from `{old_tag.capitalize()}` and assigned to `{tag.capitalize()}` tag"

# Get shiny tags
async def get_tag_hunters(server_id, tag):
    
    query = {"server_id" : server_id}

    data_cursor = mongo_manager.manager.get_all_data("tags", query)

    """
    {
        "object_id" : 100000000000000000,
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_name" : ["hunter_id_1", "hunter_id_2"]
        }
    }
    """

    tag_data = data_cursor[0]["tags"]

    try:
        hunters = tag_data[tag]
    except:
        hunters = None

    return hunters

# Get show hunters embed
async def get_show_hunters_embd(tag, hunters):

    if hunters is None:
        return await aerialace.get_info_embd("Tag not found", "No one is assigned to `{tag}` tag".format(tag=tag.capitalize()), global_vars.WARNING_COLOR)

    embd = discord.Embed(color=global_vars.NORMAL_COLOR)
    embd.title = "Users assigned to `{tag}` tag".format(tag=tag.capitalize())
    embd.description = ""

    for i in hunters:
        embd.description += "<@{hunter_id}>\n".format(hunter_id=i)

    return embd

