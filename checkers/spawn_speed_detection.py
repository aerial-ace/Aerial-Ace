from discord import Embed, Message

from config import POKETWO_ID
from managers import cache_manager
from managers.logging_manager import get_logger

logger = get_logger()

cached_server_data = {"server_id": 0}


async def get_server_spawn_speed(server_id: str) -> int:
    return cached_server_data.get(server_id, 0)


async def detect_spawn(msg: Message) -> None:

    if msg.author.id != int(POKETWO_ID):
        return

    if msg.guild is None:
        return

    if cache_manager.cached_spawnrate_data is None:
        return

    server_data = cache_manager.cached_spawnrate_data.get(str(msg.guild.id), None)

    if server_data == None or server_data.get("active") is False:
        return

    embd: Embed | None = msg.embeds[0] if len(msg.embeds) > 0 else None

    if embd is None or embd.title is None:
        return  # Doesn't contain any embed

    if embd.title.find("pokémon has appeared!") <= 0:
        return  # The embed is not a pokemon embed

    server_id = str(msg.guild.id)

    new_server_spawn_count = {server_id: cached_server_data.get(server_id, 0) + 1}

    cached_server_data.update(new_server_spawn_count)


async def reset_spawns(server_id: str):

    cached_server_data.update({server_id: 0})
