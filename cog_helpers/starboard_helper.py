from discord import TextChannel
from discord import Embed, Message
import datetime
import json

from managers import mongo_manager
from cog_helpers import general_helper
from config import NORMAL_COLOR, RARE_CATCH_COLOR, NON_SHINY_LINK_TEMPLATE, SHINY_LINK_TEMPLATE, JIRACHI_WOW, PIKA_SHOCK, DEFAULT_RARE_TEXT, DEFAULT_SHINY_TEXT

"""Sets/Resets the starboard channel"""

async def set_starboard(server_id : str, channel : TextChannel = None) -> str:

    try:
        query = {"server_id" : server_id}

        cursor = mongo_manager.manager.get_all_data("servers", query)

        server_data = cursor[0]

        # return if already enabled or disabled
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

"""Change the starboard text"""
async def set_starboard_text(server_id:str, text:str, type:str) -> Embed:
    query = {
        "server_id" : server_id
    }

    data = mongo_manager.manager.get_all_data("servers", query)[0]

    if data.get("tier", 0) < 1:
        return Embed(title="Whoops!", description="Your server is either not premium or is in lower tier. \nBecome a patron or upgrade to higher tier to access these customization!")

    if type == "RARE":
        updated_data = {
            "starboard_text_rare" : text
        }
    elif type == "SHINY":
        updated_data = {
            "starboard_text_shiny" : text
        }

    try:
        mongo_manager.manager.update_all_data("servers", query, updated_data)
        if text != "DEFAULT":
            return Embed(title=f"Starboard {type} Text Updated!")
        else:
            return Embed(title=f"Starboard {type} Text Reset")
    except Exception as e:
        return Embed(title="Error Occurred", description="```e```")

"""Change the starboard image"""
async def set_starboard_image(server_id:str, text:str, type:str) -> Embed:
    query = {
        "server_id" : server_id
    }

    data = mongo_manager.manager.get_all_data("servers", query)[0]

    if data.get("tier", 0) < 2:
        return Embed(title="Whoops!", description="Your server is either not premium or is in lower tier. \nBecome a patron or upgrade to higher tier to access these customization!")

    if type == "RARE":
        updated_data = {
            "starboard_image_rare" : text
        }
    elif type == "SHINY":
        updated_data = {
            "starboard_image_shiny" : text
        }

    try:
        mongo_manager.manager.update_all_data("servers", query, updated_data)
        if text != "DEFAULT":
            return Embed(title=f"Starboard {type} Image Updated!")
        else:
            return Embed(title=f"Starboard {type} Image Reset")
    except Exception as e:
        return Embed(title="Error Occurred", description="```e```")

"""Returns the starboard embed for starboard channel"""

async def get_starboard_embed(user_name : str, level : str, pokemon_id:str, message_link : str, is_shiny:bool = False, time:str = None):

    pokemon = pokemon_id.replace(" ", "").lower()
    pokemon = pokemon.replace("é", "e")     #This is because of you Flabébé >:|
    pokemon = pokemon.removeprefix("defense").removeprefix("attack").removeprefix("speed")

    name_aliter = {"ho-oh":"hooh"}

    try:
        pokemon = name_aliter[pokemon]
    except KeyError as e:
        
        # modify the id for alolan and galarian forms
        if pokemon.startswith("alolan"):
            pokemon = pokemon.removeprefix("alolan") + "-alola"
        elif pokemon.startswith("galarian"):
            pokemon = pokemon.removeprefix("galarian") + "-galar"
        elif pokemon.startswith("hisuian"):
            pokemon = pokemon.removeprefix("hisuian") + "-hisui"
        elif pokemon.startswith("complete"):
            pokemon = pokemon.removeprefix("complete") + "-complete"
        elif pokemon.startswith("10%"):
            pokemon = pokemon.removeprefix("10%") + "-10"

    embd = Embed()

    if is_shiny is False:
        embd.title = ":star: Rare Catch Detected :star:"
        embd.color = NORMAL_COLOR

        embd.description = f"**Trainer :** {user_name}\n"
        embd.description += f"**Pokemon :** {pokemon_id.capitalize()}\n"
        embd.description += f"**Level :** {level} [Teleport]({message_link})"

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon)
        embd.set_thumbnail(url=image_link)
    else:
        embd.title = ":sparkles: Shiny Catch Detected :sparkles:"
        embd.color = RARE_CATCH_COLOR

        embd.description = f"**Trainer :** {user_name}\n"
        embd.description += f"**Pokemon :** {pokemon_id.capitalize()}\n"
        embd.description += f"**Level :** {level} [Teleport]({message_link})"

        image_link = SHINY_LINK_TEMPLATE.format(pokemon=pokemon)
        embd.set_thumbnail(url=image_link)

    if time is not None:
        embd.set_footer(time)

    return embd

"""Sends the star catch embed to the starboard"""

async def send_starboard(server_id:str, user_id:str, level:str, pokemon:str, message:Message, is_shiny:bool, time:str = None):
    
    query = {"server_id" : server_id}

    # get starboard channel
    cursor = mongo_manager.manager.get_all_data("servers", query)
    try:
        data = cursor[0]
    except:
        print(mongo_manager.manager.db.name)
        
        print(server_id)
        return

    starboard_channel_id = data["starboard"]

    # return if module is disabled
    if starboard_channel_id == "0":
        return await general_helper.get_info_embd("No starboard channel set", "", NORMAL_COLOR)

    # get starboard embed
    reply = await get_starboard_embed(user_id, level, pokemon, message.jump_url, is_shiny, time)

    # send that starboard embed to the starboard channel
    starboard_channel : TextChannel= message.guild.get_channel(int(starboard_channel_id))
    await starboard_channel.send(embed=reply)

    return await general_helper.get_info_embd(f"This catch was sent to Starboard", f"Channel : {starboard_channel.mention}", NORMAL_COLOR)

"""returns the embed containing the rare catch info"""

async def get_rare_catch_embd(server_id:str, _ping, _pokemon, _level, is_shiny:bool):

    query = {
        "server_id" : server_id
    }

    cursor = mongo_manager.manager.get_all_data("servers", query)

    try:
        data = cursor[0]
    except:
        print(mongo_manager.manager.db.name)
        print(server_id)
        return

    tier:int = data.get("tier", 0)

    if data.get("starboard_embed", "DEFAULT") != "DEFAULT" and tier >= 3:
        data = json.loads(data.get("starboard_embed", "DEFAULT"))
        return Embed().from_dict(data)

    embd = Embed(color=RARE_CATCH_COLOR)

    if is_shiny is not True:
        embd.description = (DEFAULT_RARE_TEXT if data.get("starboard_text_rare", "DEFAULT") == "DEFAULT" or tier < 1 else data.get("starboard_text_rare", "DEFAULT")).format(ping=_ping, level=_level, pokemon=_pokemon.strip())

        embd.set_image(url=(JIRACHI_WOW if data.get("starboard_image_rare", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_rare", "DEFAULT")))
    else:
        embd.description = (DEFAULT_SHINY_TEXT if data.get("starboard_text_shiny", "DEFAULT") == "DEFAULT" or tier < 1 else data.get("starboard_text_shiny", "DEFAULT")).format(ping=_ping, level=_level, pokemon=_pokemon.strip())

        embd.set_image(url=(PIKA_SHOCK if data.get("starboard_image_shiny", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_shiny", "DEFAULT")))

    embd.timestamp = datetime.datetime.now()

    return embd