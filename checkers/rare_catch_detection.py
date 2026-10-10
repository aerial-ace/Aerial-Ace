import random
import re

import discord

import config
from helpers import general_helper, starboard_helper
from helpers.data.catch_info import CatchInfo, CatchType
from managers import cache_manager, mongo_manager
from managers.logging_manager import get_logger

logger = get_logger()


async def can_send_alert(server_details: list, catch_details: CatchInfo) -> bool:
    """
    Check if the logs are enabled in the provided server details
    Returns true if the logs are enabled for the provided catch_details, no otherwise
    """

    # fetch the server's mask
    default_mask = {"mask": "111111"}
    mask = int(server_details[0].get("alerts", default_mask).get("mask"), 2)

    # if the catch is hunt and check if hunt logs are enabled
    if catch_details.is_hunt:
        return mask & config.ALERT_TYPE_MASK.get("hunt", 0) > 0

    # if the catch is shiny and check if hunt logs are enabled
    if catch_details.is_shiny:
        return mask & config.ALERT_TYPE_MASK.get("shiny", 0) > 0

    # if the catch is gmax and check if hunt logs are enabled
    if catch_details.is_gmax:
        return mask & config.ALERT_TYPE_MASK.get("gmax", 0) > 0

    # if the catch is rare and check if hunt logs are enabled
    if catch_details.is_rare:
        if catch_details.type is CatchType.REGIONAL:
            return mask & config.ALERT_TYPE_MASK.get("regional", 0) > 0
        elif catch_details.type in (CatchType.LEGENDARY, CatchType.MYTHICAL, CatchType.ULTRABEAST):
            return mask & config.ALERT_TYPE_MASK.get("rare", 0) > 0

    # if the catch is streak and check if hunt logs are enabled
    if catch_details.streak > 0:
        return mask & config.ALERT_TYPE_MASK.get("streak", 0) > 0

    # logs are not enabled
    return False


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

    catch_info: CatchInfo | None = await fetch_catch_info(message)
    if catch_info is None:
        return  # Unable to proceed! Either not a catch or failed to get catch info

    # return if not a rare catch and not a streak and not even a low/high iv.
    # fmt: off
    if (not catch_info.is_shiny and
        not catch_info.is_hunt and
        not catch_info.is_rare and
        not catch_info.is_gmax and
        catch_info.streak == 0 and
        float(catch_info.ivs) > 10 and float(catch_info.ivs) < 90
    ):
        return
    # fmt: on

    server_details = await mongo_manager.manager.get_all_data("servers", {"server_id": str(message.guild.id)})
    if server_details is None:
        logger.error("Failed to rare check! Can't fetch server data from DB")
        return

    if catch_info.is_shiny:
        await mongo_manager.manager.increment_shiny_counter(str(message.guild.id))

    alerts_allowed: bool = await can_send_alert(server_details, catch_info)

    if alerts_allowed:
        """ Get and Send Catch Detection Embed"""
        reply: discord.Embed | None = await starboard_helper.get_rare_catch_embd(server_details, catch_info)
        if reply is None:
            ref_num = random.getrandbits(64)
            logger.error(f"Failed to get the rare catch embed! Reference Num : {ref_num}")
            logger.error(f"Catch Message was : {message.content}")
            reply_embd = await general_helper.get_error_embd("Whoops", f"Failed to get the rare catch embed! Please report this to the Support Server\b```Reference Number : {ref_num}```")
            await message.channel.send(embed=reply_embd)
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


async def fetch_catch_info(message: discord.Message) -> CatchInfo | None:
    """
    Check if any message is a rare catch message
    Return a proper dict if everything works out, empty dict if not a rare catch, None if error while determining rare catch
    """

    catch_info: CatchInfo = CatchInfo()

    msg = message.content

    catch_keywords = ["Congratulations", "You", "caught", "a", "Level"]
    shiny_keywords = ["These", "colors", "seem", "unusual"]
    hunt_keywords = ["Shiny streak reset."]

    # determines whether this message is a catch message by checking the presence of the all catch keywords
    for catch_keyword in catch_keywords:
        if catch_keyword not in msg:
            return None  # Not a catch message

    # determine shiny catch by checking the presence of all the shiny keywords
    catch_info.is_shiny = True
    for shiny_keyword in shiny_keywords:
        if shiny_keyword not in msg:
            catch_info.is_shiny = False
            break

    # Check if the catch represents a hunt completion
    catch_info.is_hunt = True
    for hunt_keyword in hunt_keywords:
        if hunt_keyword not in msg:
            catch_info.is_hunt = False
            break

    # Determine if Gmax catch or not
    gmax_regex = r"It seems that this pokémon has the Gigantamax Factor..."
    gmax_regex_outcome = re.findall(gmax_regex, msg)
    catch_info.is_gmax = len(gmax_regex_outcome) > 0

    # Set the catched pokemon Level
    level_regex = r"(?<=Level\s)\w+"
    level_regex_outcome = re.findall(level_regex, msg)
    level = level_regex_outcome[0] if len(level_regex_outcome) > 0 else 0

    if level == 0:
        logger.error(f"Pokemon level couldn't be determined from the catch message! Msg: {message.content}")
        return None

    catch_info.level = level

    # Set the catched pokemon name
    pokemon_name_regex = rf"(?<=\bLevel\s{level}\s)(.*?)(?=\s*<:)"
    pokemon_name_regex_outcome = re.findall(pokemon_name_regex, msg)
    pokemon_name = pokemon_name_regex_outcome[0] if len(pokemon_name_regex_outcome) > 0 else ""
    catch_info.pokemon = pokemon_name

    if pokemon_name == "":
        logger.error(f"Pokemon name couldn't be determined from the catch message! Msg: {message.content}")
        return None  # pokemon name couldn't be determined

    # Set the catch type
    catch_info.type = await cache_manager.fetch_poke_rarity_from_name(pokemon_name)

    catch_info.is_rare = True
    if catch_info.type is CatchType.COMMON:
        catch_info.is_rare = False

    # Set the catch IVs
    iv_regex = r"\d+(?:\.\d+)(?=%)"
    iv_regex_outcome = re.findall(iv_regex, msg)
    iv: float = float(iv_regex_outcome[0]) if len(iv_regex_outcome) > 0 else -1.0

    catch_info.ivs = iv

    # Set the Catch User
    user_regex = r"<@\d+>"
    user_regex_outcome = re.findall(user_regex, msg)
    user = user_regex_outcome[0] if len(user_regex_outcome) > 0 else None

    if user is None:
        logger.error(f"User couldn't be determined from the catch message! Msg: {message.content}")
        return None

    catch_info.user = user

    # Set the Catch Streak
    catch_streak_text = ["100th", "1,000th", "10,000th"]
    if catch_streak_text[0] in msg:
        catch_info.streak = 100
    elif catch_streak_text[1] in msg:
        catch_info.streak = 1000
    elif catch_streak_text[2] in msg:
        catch_info.streak = 10000

    return catch_info
