import json

from bot import global_vars

# data containers
cached_stats_data = {}
cached_moveset_data = {}
cached_tag_data = {}
cached_fav_data = {}
cached_battle_data = {}

# caches the data that remains unchanged
async def cache_data():
    global cached_stats_data, cached_moveset_data, cached_tag_data, cached_fav_data, cached_battle_data

    cached_stats_data = get_all_stats()
    cached_moveset_data = get_all_moveset()
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
