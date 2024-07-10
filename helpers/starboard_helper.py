from discord import TextChannel
from discord import Embed, Message
from discord import errors
import datetime
import json

from managers import mongo_manager, init_manager, cache_manager
from helpers import general_helper
from config import NORMAL_COLOR, RARE_CATCH_COLOR, SHINY_CATCH_COLOR, GMAX_CATCH_COLOR, HUNT_COMPLETED_COLOR, STREAK_COLOR, LOW_IV_COLOR, HIGH_IV_COLOR, NON_SHINY_LINK_TEMPLATE, HIGH_RES_NON_SHINY_LINK_TEMPLATE, SHINY_LINK_TEMPLATE, HIGH_RES_SHINY_LINK_TEMPLATE, JIRACHI_WOW, PIKA_SHOCK, DEFAULT_RARE_TEXT, DEFAULT_SHINY_TEXT, DEFAULT_GMAX_TEXT, STREAK_EMOJI, GMAX_EMOJI, LOW_IV_EMOJI, HIGH_IV_EMOJI, ERROR_COLOR

"""Sets/Resets the starboard channel"""


async def set_starboard(server_id: str, channel: TextChannel) -> str:
    try:
        query = {"server_id": server_id}

        cursor = await mongo_manager.manager.get_all_data("servers", query)

        server_data = cursor[0]

        # return if already enabled or disabled
        if channel is not None:
            if server_data["starboard"] == str(channel.id):
                return f"Starboard Channel is already set to {channel.mention}"
                
            updated_data = {"starboard": str(channel.id)}
        else:
            if server_data["starboard"] == "0":
                return "Starboard Module is already disabled"

            updated_data = {"starboard": "0"}

        await mongo_manager.manager.update_all_data("servers", query, updated_data)

    except Exception as e:
        return e.__str__()
    else:
        if channel is not None:
            return f"Sending rare catches to {channel.mention}"
        else:
            return "Starboard Module was disabled"


""" Sets / Disables the shiny logging channel """

async def set_shiny_starboard(server_id: str, channel: TextChannel) -> str:
    try:
        query = {"server_id": server_id}

        cursor = await mongo_manager.manager.get_all_data("servers", query)

        server_data = cursor[0]

        # return if already enabled or disabled
        if channel is not None:
            if server_data.get("shiny_starboard_channel", "0") == str(channel.id):
                return f"Shiny Starboard Channel is already set to {channel.mention}"
                
            updated_data = {"shiny_starboard_channel": str(channel.id)}
        else:
            if server_data.get("shiny_starboard_channel", "0") == "0":
                return "Shiny Starboard Module is already disabled"

            updated_data = {"shiny_starboard_channel": "0"}

        await mongo_manager.manager.update_all_data("servers", query, updated_data)

    except Exception as e:
        return e.__str__()
    else:
        if channel is not None:
            return f"Sending **SHINY** catches to {channel.mention}"
        else:
            return "Shiny Starboard Module was disabled"


""" Toggles the High Res Images"""
async def set_highres(server_id:str):
    
    query = {"server_id": server_id}

    cursor = await mongo_manager.manager.get_all_data("servers", query)

    server_data = cursor[0]
    
    if server_data.get("tier") <= 0:
        return "Not a premium server! Use `-aa premium` to know more!"
    
    updated_data = {
        "high_res" : not server_data.get("high_res", False)
    }
    
    await mongo_manager.manager.update_all_data("servers", query, updated_data)
    
    return "High Res Status : **{}**".format(not server_data.get("high_res", False))

"""Change the starboard text"""


async def set_starboard_text(server_id: str, text: str, type: str) -> Embed:
    query = {
        "server_id": server_id
    }

    data = (await mongo_manager.manager.get_all_data("servers", query))[0]

    if data.get("tier", 0) < 1:
        return Embed(title="Whoops!", description="Your server is either not premium or is in lower tier. \nBecome a patron or upgrade to higher tier to access these customization!")

    if type == "RARE":
        updated_data = {
            "starboard_text_rare": text
        }
    elif type == "SHINY":
        updated_data = {
            "starboard_text_shiny": text
        }

    try:
        await mongo_manager.manager.update_all_data("servers", query, updated_data)
        if text != "DEFAULT":
            return Embed(title=f"Starboard {type} Text Updated!")
        else:
            return Embed(title=f"Starboard {type} Text Reset")
    except Exception as e:
        return Embed(title="Error Occurred", description="```{}```".format(e))


"""Change the starboard image"""


async def set_starboard_image(server_id: str, text: str, type: str) -> Embed:
    query = {
        "server_id": server_id
    }

    data = (await mongo_manager.manager.get_all_data("servers", query))[0]

    if data.get("tier", 0) < 2:
        return Embed(title="Whoops!", description="Your server is either not premium or is in lower tier. \nBecome a patron or upgrade to higher tier to access these customization!")

    if type == "RARE":
        updated_data = {
            "starboard_image_rare": text
        }
    elif type == "SHINY":
        updated_data = {
            "starboard_image_shiny": text
        }

    try:
        await mongo_manager.manager.update_all_data("servers", query, updated_data)
        if text != "DEFAULT":
            return Embed(title=f"Starboard {type} Image Updated!")
        else:
            return Embed(title=f"Starboard {type} Image Reset")
    except Exception as e:
        return Embed(title="Error Occurred", description="```{}```".format(e))


"""Returns the starboard embed for starboard channel"""


async def get_starboard_embed(catch_details, server_details, message_link: str, tier: int = 0):

    user_name = catch_details["user"]
    level = catch_details["level"]
    pokemon_id = catch_details["pokemon"]
    iv = catch_details["iv"]
    type = catch_details["type"]
    streak = catch_details["streak"]
    is_hunt = catch_details["hunt"]

    pokemon = pokemon_id.replace(" ", "").lower()
    pokemon = pokemon.replace("é", "e")  # This is because of you Flabébé >:|
    pokemon = pokemon.removeprefix("defense").removeprefix("attack").removeprefix("speed")

    name_aliter = {
        "ho-oh": "hooh", 
        "chien-pao" : "chienpao", 
        "wo-chien" : "wochien", 
        "ting-lu" : "tinglu"
    }

    try:
        pokemon = name_aliter[pokemon]
    except KeyError:

        # modify the id for alolan and galarian forms
        if pokemon.startswith("alolan"):
            pokemon = pokemon.removeprefix("alolan") + "-alola"
        elif pokemon.startswith("galarian"):
            pokemon = pokemon.removeprefix("galarian") + "-galar"
        elif pokemon.startswith("hisuian"):
            pokemon = pokemon.removeprefix("hisuian") + "-hisui"
        elif pokemon.startswith("paldean"):
            pokemon = pokemon.removeprefix("paldean") + "-paldea"
        elif pokemon.startswith("complete"):
            pokemon = pokemon.removeprefix("complete") + "-complete"
        elif pokemon.startswith("10%"):
            pokemon = pokemon.removeprefix("10%") + "-10"

    if type == "gmax":
        pokemon = pokemon + "-gmax"

    embd = Embed()

    embd.description = f"**`Trainer :`** {user_name}\n"
    embd.description +=f"**`Pokemon :`** {pokemon_id.title()}\n"
    embd.description +=f"**`Level   :`** {level} \n"
    embd.description +=f"**`IVs     :`** {iv}% [TELEPORT]({message_link})\n\n"

    pokemon_id = cache_manager.cached_type_data[pokemon]["id"]

    high_res_enabled = server_details.get("high_res", False)

    if type == "rare":
        embd.title = ":star: Rare Catch Detected :star:"
        embd.color = RARE_CATCH_COLOR
        embd.description += ("**`Streak  :`** {streak} {emote}".format(emote=STREAK_EMOJI, streak=streak) if streak != 0 else "")

        if high_res_enabled:
            image_link = HIGH_RES_NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon_id)
        else:
            image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon)
        
    elif type == "shiny":
        if is_hunt is False:
            embd.title = ":sparkles: Shiny Catch Detected :sparkles:"
            embd.color = SHINY_CATCH_COLOR
        else:
            embd.title = ":fire: Hunt Completed :fire:"
            embd.color = HUNT_COMPLETED_COLOR

        embd.description += ("**`Streak  :`** {streak} {emote}".format(emote=STREAK_EMOJI, streak=streak) if streak != 0 else "")
        
        if high_res_enabled:
            image_link = HIGH_RES_SHINY_LINK_TEMPLATE.format(pokemon=pokemon_id)
        else:
            image_link = SHINY_LINK_TEMPLATE.format(pokemon=pokemon)

    elif type == "gmax":
        embd.title = f"{GMAX_EMOJI} GMAX Catch Detected {GMAX_EMOJI}"
        embd.color = GMAX_CATCH_COLOR
        embd.description += ("**`Streak  :`** {streak} {emote}".format(emote=STREAK_EMOJI, streak=streak) if streak != 0 else "")
        
        if high_res_enabled:
            image_link = HIGH_RES_NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon_id)
        else:
            image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon)

    elif streak != 0 and tier > 0:
        embd.title = "{emote} Catch Streak Detected {emote}".format(emote=STREAK_EMOJI)
        embd.color = STREAK_COLOR
        embd.description += "**`Streak  :`** {streak}".format(streak=streak)
        
        if high_res_enabled:
            image_link = HIGH_RES_NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon_id)
        else:
            image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon)

    else:
        ivs = float(iv)
        iv_status = "Rare Low IV" if ivs < 5 else "Rare High IV"
        iv_emote  = LOW_IV_EMOJI if ivs < 5 else HIGH_IV_EMOJI

        embd.title = "{emote} {status} Catch Detected {emote}".format(emote=iv_emote, status=iv_status)
        embd.color = LOW_IV_COLOR if ivs < 5 else HIGH_IV_COLOR
        embd.description += ("**`Streak  :`** {streak} {emote}".format(emote=STREAK_EMOJI, streak=streak) if streak != 0 else "")
        
        if high_res_enabled:
            image_link = HIGH_RES_NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon_id)
        else:
            image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon)

    embd.set_thumbnail(url=image_link)
    embd.timestamp = datetime.datetime.now()

    return embd


"""Sends the star catch embed to the starboard"""


async def send_starboard(server_details, catch_details, message:Message):

    try:
        data = server_details[0]
    except KeyError:
        data = await init_manager.register_guild_without_bs(server_details[0].get("server_id"))

    """

    0. Store the current SETTING. 
    1. Store the logging channel ID for each SETTING. 
    2. Fetch Logging channel ID based on the current SETTING. 
    3. Send the embed to fetched channel ID.

    """

    starboard_channel_id = ""

    # Tries to fetch the shiny logging channel, if it is found then set the starboard channel as the shiny channel else just set the default logging channel.
    if catch_details.get("type", "rare") == "shiny":
        starboard_channel_id = data.get("starboard") if data.get("shiny_starboard_channel", "0") == "0" else data.get("shiny_starboard_channel")
    else:
        starboard_channel_id = data.get("starboard", "0")

    tier = data.get("tier", 0)

    # return if module is disabled
    if starboard_channel_id == "0":
        return await general_helper.get_info_embd("No starboard channel set", "", NORMAL_COLOR)

    # get starboard embed
    reply = await get_starboard_embed(catch_details, server_details[0], message.jump_url, tier)

    # send that starboard embed to the starboard channel
    starboard_channel: TextChannel = message.guild.get_channel(int(starboard_channel_id))

    if starboard_channel is None:
        return await general_helper.get_info_embd("No Access", f"Can't send message in <#{starboard_channel_id}>")

    try:
        await starboard_channel.send(embed=reply)
    except errors.Forbidden:
        return await general_helper.get_info_embd(f"Missing Permissions!", f"Can't send message in <#{starboard_channel_id}>", ERROR_COLOR, "Please report this bug at the support server.")
    except Exception as e:
        return await general_helper.get_info_embd(f"Error Occurred!", f"Unable to send to Starboard. \n```{e}```", ERROR_COLOR, "Please report this bug at the support server.")

    return await general_helper.get_info_embd(f"This catch was sent to Starboard", f"Channel : {starboard_channel.mention}", NORMAL_COLOR)


"""returns the embed containing the rare catch info"""


async def get_rare_catch_embd(server_details, catch_details):

    _ping = catch_details["user"]
    _type = catch_details["type"]
    _pokemon = catch_details["pokemon"]
    _level = catch_details["level"]
    _streak = catch_details["streak"]
    _iv = catch_details["iv"]
    _hunt = catch_details["hunt"]

    try:
        data = server_details[0]
    except KeyError:
        data = await init_manager.register_guild_without_bs(server_details[0].get("server_id"))

    tier: int = data.get("tier", 0)

    if data.get("starboard_embed", "DEFAULT") != "DEFAULT" and tier >= 3:
        data = json.loads(data.get("starboard_embed", "DEFAULT"))
        return Embed().from_dict(data)

    embd = Embed()

    embd.title = "Sample Title"
    embd.description = "Sample Description"

    if _type == "rare":
        embd.title = ":star: Rare Catch Detected :star:"
        embd.color = RARE_CATCH_COLOR
        embd.description = (DEFAULT_RARE_TEXT if data.get("starboard_text_rare", "DEFAULT") == "DEFAULT" or tier < 1 else data.get("starboard_text_rare", "DEFAULT")).format(ping=_ping, level=_level, pokemon=_pokemon.strip())

        embd.description += ("\n{emote} Streak : {streak}".format(emote=STREAK_EMOJI, streak=_streak) if _streak != 0 else "")

        embd.set_image(url=(JIRACHI_WOW if data.get("starboard_image_rare", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_rare", "DEFAULT")))

    elif _type == "shiny":
        if _hunt is False:
            embd.title = ":sparkles: Shiny Catch Detected :sparkles:"
            embd.color = SHINY_CATCH_COLOR
        else:
            embd.title = ":fire: Hunt Completed :fire:"
            embd.color = HUNT_COMPLETED_COLOR

        embd.description = (DEFAULT_SHINY_TEXT if data.get("starboard_text_shiny", "DEFAULT") == "DEFAULT" or tier < 1 else data.get("starboard_text_shiny", "DEFAULT")).format(ping=_ping, level=_level, pokemon=_pokemon.strip())

        embd.description += ("\n{emote} Streak : {streak}".format(emote=STREAK_EMOJI, streak=_streak) if _streak != 0 else "")

        embd.set_image(url=(PIKA_SHOCK if data.get("starboard_image_shiny", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_shiny", "DEFAULT")))

    elif _type == "gmax":
        embd.title = f"{GMAX_EMOJI} Gmax Catch Detected {GMAX_EMOJI}"
        embd.color = GMAX_CATCH_COLOR
        embd.description = (DEFAULT_GMAX_TEXT if data.get("starboard_text_rare", "DEFAULT") == "DEFAULT" or tier < 1 else data.get("starboard_text_rare", "DEFAULT")).format(ping=_ping, level=_level, pokemon=_pokemon.strip())

        embd.description += ("\n{emote} Streak : {streak}".format(emote=STREAK_EMOJI, streak=_streak) if _streak != 0 else "")

        embd.set_image(url=(JIRACHI_WOW if data.get("starboard_image_rare", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_rare", "DEFAULT")))

    elif _streak != 0 and tier > 0:
        embd.title = f"{STREAK_EMOJI} Catch Streak {STREAK_EMOJI}"
        embd.color = STREAK_COLOR
        embd.description = "{ping} caught their {streak}th {pokemon}\n\n:tada: Congratulations :tada:".format(ping=_ping, streak=_streak, pokemon=_pokemon)

    else:
        ivs = float(_iv)
        iv_emote = LOW_IV_EMOJI if ivs < 5 else HIGH_IV_EMOJI
        
        if ivs < 5:
            iv_status = "Rare Low IV"
        elif ivs > 95:
            iv_status = "Rare High IV"
        else:
            return None # Return None if no case is matched.

        embd.title = f"{iv_emote} {iv_status} Catch Detected {iv_emote}"
        embd.color = LOW_IV_COLOR if ivs < 5 else HIGH_IV_COLOR
        embd.description = "{ping} caught a {status} Pokemon\n\n:tada: Congratulations :tada:".format(ping=_ping, streak=_streak, pokemon=_pokemon, status=iv_status)
        embd.set_image(url=(JIRACHI_WOW if data.get("starboard_image_rare", "DEFAULT") == "DEFAULT" or tier < 2 else data.get("starboard_image_rare", "DEFAULT")))

    embd.timestamp = datetime.datetime.now()

    return embd

async def send_sample(server_id):

    query = {
        "server_id": str(server_id)
    }

    cursor = await mongo_manager.manager.get_all_data("servers", query)

    data = cursor[0] if len(cursor) > 0 else None

    return data.get("starboard") if data is not None else None   
