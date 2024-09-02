import json
from managers import mongo_manager

import config

# data containers
cached_stats_data = None
cached_moveset_data = None
cached_alt_name_data = None
cached_rarity_data = None
cached_nature_data = None
cached_type_data = None
cached_weakness_data = None
cached_duelish_data = None

cached_spawnrate_data = None
cached_shinycounter_data = None


async def search_cached_type_data(name: str) -> dict:
    
    global cached_type_data
    
    type_data_aliter = {
        "darmanitan" : "darmanitan-standard",
        "darmanitan-galar" : "darmanitan-galar-standard",
        "deoxys" : "deoxys-normal",
        "meloetta" : "meloetta-aria",
        "zygarde" : "zygarde-50"
    }
    
    try:
        aliter = type_data_aliter[name]
        return cached_type_data.get(aliter)
    except KeyError as k:
        try:
            return cached_type_data.get(name)
        except KeyError as kk:
            print(f">>>>> {name} is not present in cached_type_data")
            return None    

async def cache_data():
    global cached_stats_data, cached_moveset_data, cached_alt_name_data, cached_rarity_data, cached_nature_data, cached_weakness_data, cached_type_data, cached_duelish_data, cached_spawnrate_data, cached_shinycounter_data

    cached_stats_data = get_all_stats()
    cached_moveset_data = get_all_moveset()
    cached_alt_name_data = get_all_alt_names()
    cached_rarity_data = get_all_rarity_data()
    cached_nature_data = get_all_nature_data()
    cached_type_data = get_all_type_data()
    cached_weakness_data = get_all_weakness_data()
    cached_duelish_data = get_all_duelish_data()

    cached_spawnrate_data = await fetch_spawnrate_info()
    cached_shinycounter_data = await fetch_shinycounter_info()

def get_all_stats():
    stats_file = open(config.STATS_FILE_LOCATION, "r")
    stats_data_raw = stats_file.read()
    stats_data = json.loads(stats_data_raw)

    return stats_data

def get_all_moveset():
    ms_file = open(config.MOVESET_FILE_LOCATION, "r")
    ms_data_raw = ms_file.read()
    ms_data = json.loads(ms_data_raw)

    return ms_data

def get_all_alt_names():
    alt_name_file = open(config.ALT_NAME_FILE_LOCATION, "r")
    alt_name_data = json.loads(alt_name_file.read())

    return alt_name_data

def get_all_rarity_data():
    rarity_file = open(config.RARITY_FILE_LOCATION, "r")
    rarity_data = json.loads(rarity_file.read())

    return rarity_data

def get_all_nature_data():
    nature_file = open(config.NATURE_FILE_LOCATION, "r")
    nature_data = json.loads(nature_file.read())

    return nature_data

def get_all_type_data():
    with open(config.TYPE_FILE_LOCATION, "r") as type_file:
        type_data = json.loads(type_file.read())

        return type_data

def get_all_weakness_data():
    with open(config.WEAKNESS_FILE_LOCATION, "r") as weakness_file:
        weakness_data = json.loads(weakness_file.read())

        return weakness_data

def get_all_duelish_data():
    with open(config.DUELISH_POKEMON_FILE_LOCATION, "r") as duelish_file:
        duelish_data = json.loads(duelish_file.read())

        return duelish_data
    
async def fetch_spawnrate_info():

    storage = {

    }

    data = await mongo_manager.manager.get_all_data("spawnrate", {})

    for x in data:
        storage.update({x.get("server_id") : {
            "active" : x.get("active"),
            "channel_id" : x.get("channel_id")
        }})

    return storage

async def fetch_shinycounter_info():

    storage = {

    }

    data = await mongo_manager.manager.get_all_data("shinycounter", {})

    for x in data:
        storage.update({x.get("server_id") : {
            "active" : x.get("active"),
            "channel_id" : x.get("channel_id"),
            "count" : x.get("count")
        }})

    return storage

async def update_spawnrates(server_id:str, active:bool, channel_id:str):

    global cached_spawnrate_data

    prev_data = cached_spawnrate_data.get(server_id, None)

    updated_data = {
        "active" : active if active is not None else False if prev_data is None else prev_data.get("active"), 
        "channel_id" : channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"),
    }

    # Return None if the new data is same as the current data.
    if prev_data == updated_data:
        return None

    cached_spawnrate_data.update({server_id : updated_data})

    return updated_data

async def update_shinycounter(server_id:str, active:bool, channel_id:str):

    global cached_shinycounter_data

    prev_data = cached_shinycounter_data.get(server_id, None)

    updated_data = {
        "active" : active if active is not None else False if prev_data is None else prev_data.get("active"), 
        "channel_id" : channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"),
        "count" : 0
    }

    # Return None if the new data is same as the current data.
    if prev_data == updated_data:
        return None

    cached_shinycounter_data.update({server_id : updated_data})

    return updated_data

async def increment_shiny_counter(server_id):

    global cached_shinycounter_data

    server_data = cached_shinycounter_data.get(str(server_id), None)

    if server_data is None:
        return    
        
    server_data["count"] = server_data["count"] + 1
        
    cached_shinycounter_data.update({
        server_id : server_data
    })