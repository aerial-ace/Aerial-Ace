import json
import logging
import pdb

from pymongo import MongoClient, collection, database

from managers import mongo_manager
from helpers import general_helper
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


def search_cached_type_data(name: str) -> dict:
    global cached_type_data

    type_data_aliter = {"darmanitan": "darmanitan-standard", "darmanitan-galar": "darmanitan-galar-standard", "deoxys": "deoxys-normal", "meloetta": "meloetta-aria", "zygarde": "zygarde-50"}

    try:
        aliter = type_data_aliter[name]
        return cached_type_data.get(aliter)
    except KeyError:
        try:
            return cached_type_data.get(name)
        except KeyError:
            logging.critical(f"{name} is not present in cached_type_data")
            return None


def cache_data():
    """Only caches the local data files. Use init() to cache the database collections as well"""

    global cached_stats_data, cached_moveset_data, cached_alt_name_data, cached_rarity_data, cached_nature_data, cached_weakness_data, cached_type_data, cached_duelish_data

    cached_stats_data = get_all_stats()
    cached_moveset_data = get_all_moveset()
    cached_alt_name_data = get_all_alt_names()
    cached_rarity_data = get_all_rarity_data()
    cached_nature_data = get_all_nature_data()
    cached_type_data = get_all_type_data()
    cached_weakness_data = get_all_weakness_data()
    cached_duelish_data = get_all_duelish_data()


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


class CacheManager:
    aerial_ace_db: database.Database = None
    servers_collection: collection.Collection = None
    spawnrate_collection: collection.Collection = None
    shinycounter_collection: collection.Collection = None

    servers_cache: dict = {}

    cached_spawnrate_data: dict = None
    cached_shinycounter_data: dict = None

    def __init__(self):
        """Connect to the sync mongoclient and cache the collections"""

        client: MongoClient = MongoClient(config.MONGO_URI)
        self.aerial_ace_db = client[config.DB]
        self.servers_collection = self.aerial_ace_db["servers"]
        self.spawnrate_collection = self.aerial_ace_db["spawnrate"]
        self.shinycounter_collection = self.aerial_ace_db["shinycounter"]

        self.cache_spawnrate_collection()
        self.cache_shinycounter_collection()

        self.cache_servers_collection()

    def cache_servers_collection(self) -> None:
        """Cache the entire servers collection"""

        documents_cursor = self.servers_collection.find({}, {"_id": 0})
        documents: list[dict] = list(documents_cursor)

        for i, doc in enumerate(documents):
            item: dict = {doc.get("server_id"): doc}
            self.servers_cache.update(item)

    async def get_server(self, server_id: int) -> dict | None:
        return self.servers_cache.get(str(server_id), None)

    def cache_spawnrate_collection(self):
        """Fetch and Cache entire spawnrate collection"""

        storage = {}
        data = list(self.spawnrate_collection.find({}, {"_id": 0}))

        for x in data:
            storage.update({x.get("server_id"): x})

        self.cached_spawnrate_data = storage

    def fetch_shinycounter_collection(self):
        """Fetch and Cache entire shinycounter collection"""

        storage = {}
        data = list(self.shinycounter_collection.find({}, {"_id": 0}))

        for x in data:
            storage.update({x.get("server_id"): x})

        self.cached_shinycounter_data = storage

    async def update_spawnrates(self, server_id: str, active: bool, channel_id: str) -> dict:
        """Update the spawnrate data to change the active status or channnel"""

        prev_data = self.cached_spawnrate_data.get(server_id, None)

        updated_data = {
            "server_id": server_id,
            "active": active if active is not None else False if prev_data is None else prev_data.get("active"),
            "channel_id": channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"),
        }

        # Return None if the new data is same as the current data.
        if prev_data == updated_data:
            return None

        self.cached_spawnrate_data.update({server_id: updated_data})

        return updated_data

    async def update_shinycounter(self, server_id: str, active: bool, channel_id: str) -> dict:
        """Update shiny counter details at both cache and db"""

        prev_data = cached_shinycounter_data.get(server_id, None)

        updated_data = {
            "server_id": server_id,
            "active": active if active is not None else False if prev_data is None else prev_data.get("active"),
            "channel_id": channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"),
            "count": 0,
        }

        # Return None if the new data is same as the current data.
        if prev_data == updated_data:
            return None

        # update the db
        await mongo_manager.manager.update_all_data("shinycounter", {"server_id": server_id}, updated_data)

        # local cache updated
        self.cached_shinycounter_data.update({server_id: updated_data})

        return updated_data

    async def increment_shiny_counter(self, server_id):
        server_data = self.cached_shinycounter_data.get(str(server_id), None)

        if server_data is None:
            return

        server_data["count"] = server_data["count"] + 1

        # update the db
        await mongo_manager.manager.update_all_data("shinycounter", {"server_id": server_id}, updated_data=server_data)

        # local cache updated
        cached_shinycounter_data.update({server_id: server_data})


manager: CacheManager = None


@general_helper.exec_time
def init():
    global manager

    manager = CacheManager()
    cache_data()
