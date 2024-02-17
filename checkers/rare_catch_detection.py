import discord
import random
import re

from managers import cache_manager, mongo_manager
from helpers import starboard_helper, general_helper
import config



async def rare_check(bot: discord.AutoShardedBot, message: discord.Message):
    """detect rare catch message"""

    bot_member: discord.Member = message.guild.get_member(bot.user.id)

    if message.channel.permissions_for(bot_member).send_messages is False:
        return

    # if str(message.author.id) != config.POKETWO_ID:
    #     return

    catch_info = await determine_rare_catch(message)

    # return if not a rare catch or a streak
    if catch_info is None or (catch_info["type"] == "" and catch_info["streak"] == 0):
        return None

    server_details = await mongo_manager.manager.get_all_data("servers", {
        "server_id": str(message.guild.id)
    })

    """ Get and Send Catch Detection Embed"""
    reply = await starboard_helper.get_rare_catch_embd(server_details, catch_info)

    if reply is None:
        return
    
    try:
        await message.channel.send(embed=reply)
    except discord.errors.Forbidden:
        return  # return if not allowed to send messages in the current channel

    """ Send Customization Reminder for non premium servers"""
    customization_reminder_possibility = 30

    if server_details[0].get("tier") == 0 and random.randint(0, 99) < customization_reminder_possibility:
        embd = await general_helper.get_info_embd(f"{config.AERIAL_ACE_EMOJI} Customize Starboard Embed!", "Enhance the starboard embed using various customization features available to premium servers. Get premium now and customize your starboard embeds to suit your servers. ", config.DEFAULT_COLOR, "Use -aa premium or join support server to know more.")
        await message.channel.send(embed=embd)

    
    """ Send the starboard embed in the starboard channel """
    starboard_reply = await starboard_helper.send_starboard(server_details, catch_info, message)

    """ Send feedback in the current channel """
    await message.channel.send(embed=starboard_reply)

async def determine_rare_catch(message:discord.Message):
    """check if any message is a rare catch message"""

    catch_info = {}

    msg = message.content

    is_shiny = True
    is_hunt = False

    catch_keywords = ["Congratulations", "You", "caught", "a", "Level"]
    shiny_keywords = ["These", "colors", "seem", "unusual"]
    hunt_keywords  = ["+1 Shiny chain!", "Shiny streak reset."]

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

    level_regex = r"(?<=Level\s)\w+"
    level_regex_outcome = re.findall(level_regex, msg)
    level = level_regex_outcome[0] if len(level_regex_outcome) > 0 else 0

    pokemon_name_regex = fr"(?<=\bLevel\s{level}\s)(.*?)(?=\s*<:)"
    pokemon_name_regex_outcome = re.findall(pokemon_name_regex, msg)
    pokemon_name = pokemon_name_regex_outcome[0] if len(pokemon_name_regex_outcome) > 0 else None

    iv_regex = r"\d+(?:\.\d+)%"
    iv_regex_outcome = re.findall(iv_regex, msg)
    iv = iv_regex_outcome[0] if len(iv_regex_outcome) > 0 else "0%"

    user = message.mentions[0].mention

    catch_streak_text = ["100th", "1000th", "10000th"]

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
    else:
        for i in pokemon_name.lower().split():
            try:
                if i == "galarian" or i == "alolan" or i == "hisuian" or cache_manager.cached_rarity_data[i] in ["legendary", "mythical", "ultra beast"]:
                    catch_info["type"] = "rare"
            except Exception:
                continue

    return catch_info
