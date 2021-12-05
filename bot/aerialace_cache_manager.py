import json

from bot import global_vars

# data containers
cached_stats_data = None
cached_moveset_data = None
cached_tag_data = None
cached_fav_data = None
cached_battle_data = None
cached_alt_name_data = None
cached_rarity_data = None

# caches the data
async def cache_data(init=False):
    global cached_stats_data, cached_moveset_data, cached_tag_data, cached_fav_data, cached_battle_data, cached_alt_name_data, cached_rarity_data

    # static
    if init is True:
        cached_stats_data = get_all_stats()
        cached_moveset_data = get_all_moveset()
        cached_alt_name_data = get_all_alt_names()
        cached_rarity_data = get_all_rarity_data()

    # dynamic
    cached_tag_data = get_all_tags()
    cached_fav_data = get_all_favs()
    cached_battle_data = get_all_battles()

# returns all the stats from stats file
def get_all_stats():
    stats_file = open(global_vars.STATS_FILE_LOCATION, "r")
    stats_data_raw = stats_file.read()
    stats_data = json.loads(stats_data_raw)

    return stats_data

# return all the moveset from the moveset file
def get_all_moveset():
    ms_file = open(global_vars.MOVESET_FILE_LOCATION, "r")
    ms_data_raw = ms_file.read()
    ms_data = json.loads(ms_data_raw)

    return ms_data

# return all tags from the tag file
def get_all_tags():
    tag_file = open(global_vars.TAG_FILE_LOCATION, "r")
    tag_data_raw = tag_file.read()
    tag_data = json.loads(tag_data_raw)

    return tag_data

# return all the battles from the battle file
def get_all_battles():
    battle_file = open(global_vars.BATTLE_LOG_FILE_LOCATION, "r")
    battle_data = json.loads(battle_file.read())

    return battle_data

# returns all the favs from the fav file
def get_all_favs():
    fav_file = open(global_vars.FAV_FILE_LOCATION, "r")
    fav_file_data = json.loads(fav_file.read())

    return fav_file_data

# returns all the alt names from the alt name file
def get_all_alt_names():
    alt_name_file = open(global_vars.ALT_NAME_FILE_LOCATION, "r")
    alt_name_data = json.loads(alt_name_file.read())

    return alt_name_data

# returns all the rarity data from the rarity file
def get_all_rarity_data():
    rarity_file = open(global_vars.RARITY_FILE_LOCATION, "r")
    rarity_data = json.loads(rarity_file.read())

    return rarity_data
