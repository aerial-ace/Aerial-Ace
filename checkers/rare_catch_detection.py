import random
import re

import discord

import config
from helpers import general_helper, starboard_helper
from managers import cache_manager, mongo_manager
from managers.logging_manager import get_logger

logger = get_logger()


async def can_send_alert(server_details: list, catch_details: dict) -> bool:

    # fetch the server's mask
    default_mask = {"mask": "111111"}
    mask = int(server_details[0].get("alerts", default_mask).get("mask"), 2)

    # if the catch is streak, check and return if the hunt streak is ON
    if catch_details.get("streak"):
        return mask & config.ALERT_TYPE_MASK.get("streak", 0) > 0

    # if the catch is hunt, check and return if the hunt bit is ON
    if catch_details.get("hunt"):
        return mask & config.ALERT_TYPE_MASK.get("hunt", 0) > 0

    # Fetch the type of catch from the catch details
    catch_type = catch_details.get("type", None)
    if catch_type is None:
        logger.error("Catch Type not found in catch details")
        return False

    # Fetch the alert mask bit from the alert type mask storage
    alert_mask: int | None = config.ALERT_TYPE_MASK.get(catch_type, None)
    if alert_mask is None:
        logger.error("Catch Type is not registered in ALERT_TYPE_MASK")
        return False

    return (mask & alert_mask) > 0


async def rare_check(_bot: discord.AutoShardedBot, message: discord.Message):
    """detect rare catch message"""

    if message.guild is None or _bot.user is None:
        return

    bot_member: discord.Member | None = message.guild.get_member(_bot.user.id)
    if bot_member is None:
        return

    # Return if not a proper text channel
    if not isinstance(message.channel, discord.TextChannel):
        return

    if message.channel.permissions_for(bot_member).send_messages is False:
        return

    if str(message.author.id) != config.POKETWO_ID:
        return

    catch_info = await determine_rare_catch(message)

    # return if not a rare catch and not a streak and not even a low/high iv.
    if catch_info is None or (catch_info["type"] == "" and catch_info["streak"] == 0 and float(catch_info["iv"]) > 10 and float(catch_info["iv"]) < 90):
        return

    server_details = await mongo_manager.manager.get_all_data("servers", {"server_id": str(message.guild.id)})
    if server_details is None:
        logger.error("Failed to rare check! Can't fetch server data from DB")
        return

    if catch_info.get("type") == "shiny":
        await mongo_manager.manager.increment_shiny_counter(str(message.guild.id))

    alerts_allowed = await can_send_alert(server_details, catch_info)

    if alerts_allowed:
        """ Get and Send Catch Detection Embed"""
        reply = await starboard_helper.get_rare_catch_embd(server_details, catch_info)

        if reply is None:
            return

        try:
            await message.channel.send(embed=reply)
        except discord.errors.Forbidden:
            return  # return if not allowed to send messages in the current channel

        """ Send the starboard embed in the starboard channel """
        starboard_reply: discord.Embed | None = await starboard_helper.send_starboard(server_details, catch_info, message)
        if starboard_reply is None:
            logger.error("Failed to send starboard reply because no proper starboar reply!")
            logger.error(f"Rare catch message was : {message.content}")
            return

        await message.channel.send(embed=starboard_reply)

    """ Send Customization Reminder for non premium servers"""
    customization_reminder_possibility = 30

    if server_details[0].get("tier", 0) == 0 and random.randint(0, 99) < customization_reminder_possibility:
        embd = await general_helper.get_info_embd(f"{config.AERIAL_ACE_EMOJI} Customize Starboard Embed!", "Enhance the starboard embed using various customization features available to premium servers. Get premium now and customize your starboard embeds to suit your servers. ", config.DEFAULT_COLOR, "Use -aa premium or join support server to know more.")
        await message.channel.send(embed=embd)


async def determine_rare_catch(message: discord.Message):
    """check if any message is a rare catch message"""

    catch_info = {}

    msg = message.content

    is_shiny = True
    is_hunt = False
    is_gmax = False

    catch_keywords = ["Congratulations", "You", "caught", "a", "Level"]
    shiny_keywords = ["These", "colors", "seem", "unusual"]
    hunt_keywords = ["Shiny streak reset."]

    # determines whether this message is a catch message by checking the presence of the all catch keywords
    for catch_keyword in catch_keywords:
        if catch_keyword not in msg:
            return None  # Not a catch message

    # determine shiny catch by checking the presence of all the shiny keywords
    for shiny_keyword in shiny_keywords:
        if shiny_keyword not in msg:
            is_shiny = False
            break

    for hunt_keyword in hunt_keywords:
        if hunt_keyword in msg:
            is_hunt = True
            break

    gmax_regex = r"It seems that this pokémon has the Gigantamax Factor..."
    gmax_regex_outcome = re.findall(gmax_regex, msg)
    is_gmax = len(gmax_regex_outcome)

    level_regex = r"(?<=Level\s)\w+"
    level_regex_outcome = re.findall(level_regex, msg)
    level = level_regex_outcome[0] if len(level_regex_outcome) > 0 else 0

    if level == 0:
        return

    pokemon_name_regex = rf"(?<=\bLevel\s{level}\s)(.*?)(?=\s*<:)"
    pokemon_name_regex_outcome = re.findall(pokemon_name_regex, msg)
    pokemon_name = pokemon_name_regex_outcome[0] if len(pokemon_name_regex_outcome) > 0 else None

    if pokemon_name is None:
        return None

    iv_regex = r"\d+(?:\.\d+)(?=%)"
    iv_regex_outcome = re.findall(iv_regex, msg)
    iv = iv_regex_outcome[0] if len(iv_regex_outcome) > 0 else "0"

    if iv == "0":
        return None

    user_regex = r"<@\d+>"
    user_regex_outcome = re.findall(user_regex, msg)
    user = user_regex_outcome[0] if len(user_regex_outcome) > 0 else None

    if user is None:
        return

    catch_streak_text = ["100th", "1,000th", "10,000th"]

    streak = 0

    if catch_streak_text[0] in msg:
        streak = 100
    elif catch_streak_text[1] in msg:
        streak = 1000
    elif catch_streak_text[2] in msg:
        streak = 10000

    catch_info["user"] = user
    catch_info["level"] = level
    catch_info["pokemon"] = pokemon_name
    catch_info["iv"] = iv

    catch_info["type"] = ""
    catch_info["streak"] = streak
    catch_info["hunt"] = is_hunt

    if is_shiny:
        catch_info["type"] = "shiny"
        return catch_info
    elif is_gmax:
        catch_info["type"] = "gmax"
        return catch_info
    else:
        for i in pokemon_name.lower().split():
            try:
                if i == "galarian" or i == "alolan" or i == "hisuian":
                    catch_info["type"] = "regional"
                if cache_manager.cached_rarity_data[i] in ["legendary", "mythical", "ultra beast"]:
                    catch_info["type"] = "rare"
            except Exception:  # noqa: BLE001, S112
                continue

    return catch_info
