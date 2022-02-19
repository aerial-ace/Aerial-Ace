from discord import TextChannel
from discord import Embed, Message

from managers import mongo_manager
from managers import cache_manager
from config import NORMAL_COLOR

async def set_starboard(server_id : str, channel : TextChannel = None):

    try:
        query = {"server_id" : server_id}

        cursor = mongo_manager.manager.get_all_data("servers", query)

        server_data = cursor[0]

        if channel is not None:
            if server_data["starboard"] == str(channel.id):
                return f"Starboard Channel is already set to {channel.mention}"
        else:
            if server_data["starboard"] == "0":
                return "Starboard Module is already disabled"

        """
        {
            "server_name" : "name",
            "server_id" : "id",
            "starboard" : "1231232323231231321"
        }
        """

        if channel is not None:
            updated_data = {"starboard" : str(channel.id)}
        else:
            updated_data = {"starboard" : "0"}

        mongo_manager.manager.update_all_data("servers", query, updated_data)

    except Exception as e:
        return e
    else:
        if channel is not None:
            return f"Sending rare catches to {channel.mention}"
        else:
            return "Starboard Module was disabled"

# returns the starboard embed for starboard channel
async def get_starboard_embed(user_id : str, level : str, pokemon_id:str, message_link : str, is_shiny:bool = False):

    try:
        pokemon_id = cache_manager.cached_alt_name_data[pokemon_id.lower()].replace("-koko", "koko").replace("-lele", "lele").replace("-bulu", "bulu").replace("-fini", "fini")
    except Exception as e:
        pokemon_id = pokemon_id.replace(" ", "").lower()

    embd = Embed(color=NORMAL_COLOR)

    if is_shiny is False:
        embd.title = ":star2: Rare Catch Detected :star2:"
        embd.description = f"{user_id} caught a level {level} `{pokemon_id.strip().capitalize()}`\n\n"
        embd.description += f"[**Teleport**]({message_link})"
        image_link = f"https://play.pokemonshowdown.com/sprites/gen5/{pokemon_id}.png"
        embd.set_thumbnail(url=image_link)
    else:
        embd.title = ":star2: Shiny Catch Detected :star2:"
        embd.description = f"{user_id} caught a level {level} **SHINY** `{pokemon_id.capitalize()}`\n\n"
        embd.description += f"[**Teleport**]({message_link})"
        image_link = f"https://play.pokemonshowdown.com/sprites/gen5-shiny/{pokemon_id}.png"
        embd.set_thumbnail(url=image_link)

    return embd

async def send_starboard(server_id:str, user_id:str, level:str, pokemon:str, message:Message, is_shiny:bool):
    
    query = {"server_id" : server_id}

    # get starboard channel
    cursor = mongo_manager.manager.get_all_data("servers", query)
    data = cursor[0]
    starboard_channel_id = data["starboard"]

    if starboard_channel_id == "0":
        return

    # get starboard embed
    reply = await get_starboard_embed(user_id, level, pokemon, message.jump_url, is_shiny)

    # send that starboard embed to the starboard channel
    await message.guild.get_channel(int(starboard_channel_id)).send(embed=reply)