from discord import Message, Embed

from managers import cache_manager
from config import POKETWO_ID

cached_server_data = {"server_id": 0}


async def get_server_spawn_speed(server_id: str) -> int:
    """Return the spawn count in the locally maintained cache of server-spawnrate count"""

    return cached_server_data.get(server_id, 0)


async def detect_spawn(msg: Message) -> None:
    """Detects if a message is a spawn message and updates the locally maintained spawn-rate counter"""

    # if empty cache, return
    if cache_manager.manager.cached_spawnrate_data is None:
        return

    server_data = cache_manager.manager.cached_spawnrate_data.get(str(msg.guild.id), None)

    # if spawnrate module is disabled, return
    if server_data is None or server_data.get("active") is False:
        return

    if msg.author.id != int(POKETWO_ID):
        return

    embd: Embed = msg.embeds[0] if len(msg.embeds) > 0 else None

    if embd is None:
        return

    if "pokémon has appeared!" not in embd.title:
        return

    server_id = str(msg.guild.id)

    new_server_spawn_count = {server_id: cached_server_data.get(server_id, 0) + 1}

    # update the local cache
    cached_server_data.update(new_server_spawn_count)


async def reset_spawns(server_id: str):
    """Resets the number of active spawns for a given server in the local cache"""

    cached_server_data.update({server_id: 0})
