import json

import config
from managers import mongo_manager
from managers.logging_manager import get_logger

logger = get_logger()

# data containers
cached_stats_data: dict[str, str] = {}
cached_moveset_data: dict[str, str] = {}
cached_alt_name_data: dict[str, str] = {}
cached_rarity_data: dict[str, str] = {}
cached_nature_data: dict[str, str] = {}
cached_type_data: dict[str, dict] = {}
cached_weakness_data: dict[str, dict] = {}
cached_duelish_data: dict[str, dict] = {}

cached_spawnrate_data: dict[str, dict] = {}
cached_shinycounter_data: dict[str, dict] = {}


async def search_cached_type_data(name: str) -> dict | None:
    """Return the type data of the poemon; if type data is not found, return None"""

    global cached_type_data  # noqa: PLW0602

    # fmt: off
    type_data_aliter = {
        "darmanitan": "darmanitan-standard", 
        "nidoran" : "nidoran-f",
        "mr.mime-galar": "mr-mime-galar",
        "darmanitan-galar": "darmanitan-galar-standard", 
        "deoxys": "deoxys-normal", 
        "wormadam": "wormadam-sandy",
        "meloetta": "meloetta-aria", 
        "giratina": "giratina-origin",
        "basculin": "basculin-red-striped",
        "tornadus": "tornadus-incarnate",
        "thundurus": "thundurus-incarnate",
        "landorus": "landorus-incarnate",
        "keldeo" : "keldeo-ordinary",
        "meowstic": "meowstic-female",
        "aegislash": "aegislash-shield",
        "pumpkaboo": "pumkaboo-average",
        "gourgiest": "gourgiest-average",
        "zygarde": "zygarde-50", 
        "oricorio": "oricorio-baile",
        "tapukoko": "tapu-koko",
        "lycanroc": "lycanroc-midday",
        "wishiwashi": "wishiwashi-solo",
        "mimikyu": "mimikyu-busted",
        "magearna": "magearna-original",
        "necrozma": "necrozma-ultra",
        "cramorant": "cramorant-gulping",
        "toxtricity": "toxtricity-amped",
        "eiscue": "eiscue-ice",
        "indeedee": "indeedee-female",
        "rapidstrikeurshifu": "urshifu-rapid-strike", 
        "singlestrikeurshifu": "urshifu-single-strike",
        "basculegion": "basculegion-female",
        "enamorous": "enamorous-incarnate",
        "shaymin": "shaymin-land",
        "zenithmarshadow": "marshadow",
        "wellspringmaskogerpon": "ogerpon-wellspring-mask",
        "hearthflamemaskogerpon": "ogerpon-hearthflame-mask",
        "cornerstonemaskogerpon": "ogerpon-cornerstone-mask",
        "neutralxerneas": "xerneas",
        "zendarmanitan-galar": "darmanitan-galar-zen",
    }
    # fmt: on

    type_data: dict | None = {}

    # if aliter name exists, then use that to fetch from catched_type_data; otherwise use the provided name
    aliter = type_data_aliter.get(name, None)
    if aliter is not None:
        type_data = cached_type_data.get(aliter, None)
    else:
        type_data = cached_type_data.get(name, None)

    # if neither the provided name or the aliter exist in cached_type_data;
    if type_data is None:
        logger.error(f"{name} is not present in cached_type_data")

    return type_data


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

    # Cache the spawn rate data
    spawnrate_data: dict | None = await fetch_spawnrate_info()
    if spawnrate_data is None:
        logger.error("Failed to cache the spawnrate data")
    else:
        cached_spawnrate_data = spawnrate_data

    # Cache the shiny counter data
    shinycounter_data: dict | None = await fetch_shinycounter_info()
    if shinycounter_data is None:
        logger.error("Failed to cache the shinycounter data")
    else:
        cached_shinycounter_data = shinycounter_data

    logger.info("Data Cached!")


def get_all_stats():
    with open(config.STATS_FILE_LOCATION, "r") as stats_file:
        stats_data_raw = stats_file.read()
        stats_data = json.loads(stats_data_raw)
        return stats_data


def get_all_moveset():
    with open(config.MOVESET_FILE_LOCATION, "r") as ms_file:
        ms_data_raw = ms_file.read()
        return json.loads(ms_data_raw)


def get_all_alt_names():
    with open(config.ALT_NAME_FILE_LOCATION, "r") as alt_name_file:
        return json.loads(alt_name_file.read())


def get_all_rarity_data():
    with open(config.RARITY_FILE_LOCATION, "r") as rarity_file:
        return json.loads(rarity_file.read())


def get_all_nature_data():
    with open(config.NATURE_FILE_LOCATION, "r") as nature_file:
        return json.loads(nature_file.read())


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


async def fetch_spawnrate_info() -> dict[str, dict] | None:
    """
    Fetch spawnrate data from db
    Return dict of data if successfull, None otherwise
    """

    storage = {}

    data = await mongo_manager.manager.get_all_data("spawnrate", {})
    if data is None:
        logger.error("Failed to fetch spawn rate data!")
        return None

    for x in data:
        storage.update({x.get("server_id"): {"active": x.get("active"), "channel_id": x.get("channel_id")}})

    return storage


async def fetch_shinycounter_info() -> dict[str, dict] | None:
    """
    Fetch the shiny counter data from db
    Return dict of data if successfull, None otherwise
    """

    storage = {}

    data = await mongo_manager.manager.get_all_data("shinycounter", {})
    if data is None:
        logger.error("Failed to fetch shiny counter data!")
        return None

    # Only store the required data in the memory, discard the _id etc from the cursor
    for x in data:
        storage.update({x.get("server_id"): {"active": x.get("active"), "channel_id": x.get("channel_id"), "count": x.get("count")}})

    return storage


async def update_spawnrates(server_id: str, active: bool | None, channel_id: str | None) -> dict | None:

    global cached_spawnrate_data

    prev_data = cached_spawnrate_data.get(server_id, None)

    updated_data = {
        "active": active if active is not None else False if prev_data is None else prev_data.get("active"),
        "channel_id": channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"),
    }

    # Return None if the new data is same as the current data.
    if prev_data == updated_data:
        return None

    cached_spawnrate_data.update({server_id: updated_data})

    return updated_data


async def update_shinycounter(server_id: str, active: bool, channel_id: str) -> dict | None:

    global cached_shinycounter_data

    prev_data = cached_shinycounter_data.get(server_id, None)

    updated_data = {"active": active if active is not None else False if prev_data is None else prev_data.get("active"), "channel_id": channel_id if channel_id is not None else "" if prev_data is None else prev_data.get("channel_id"), "count": 0}

    # Return None if the new data is same as the current data.
    if prev_data == updated_data:
        return None

    cached_shinycounter_data.update({server_id: updated_data})

    return updated_data


async def increment_shiny_counter(server_id) -> bool:

    global cached_shinycounter_data

    server_data = cached_shinycounter_data.get(str(server_id), None)

    if server_data is None:
        return False

    server_data["count"] = server_data["count"] + 1

    cached_shinycounter_data.update({server_id: server_data})

    return True
