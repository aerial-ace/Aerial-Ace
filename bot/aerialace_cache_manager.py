import json

from bot import global_vars

# data containers
cached_stats_data = None
cached_moveset_data = None
cached_alt_name_data = None
cached_rarity_data = None

# caches the data
async def cache_data(init=False):
    global cached_stats_data, cached_moveset_data, cached_alt_name_data, cached_rarity_data

    cached_stats_data = get_all_stats()
    cached_moveset_data = get_all_moveset()
    cached_alt_name_data = get_all_alt_names()
    cached_rarity_data = get_all_rarity_data()

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
