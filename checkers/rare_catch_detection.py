import discord
import datetime

from cog_helpers import starboard_helper
from managers import cache_manager
import config

"""detect rare catch message"""

async def rare_check(message : discord.Message):    
    if str(message.author.id) != config.POKETWO_ID:
        return

    catch_info = await determine_rare_catch(message.content)

    # return if not a rare catch
    if catch_info is None or (catch_info["type"] == "" and catch_info["streak"] == 0):
        return None

    # get the rare catch details
    reply = await starboard_helper.get_rare_catch_embd(str(message.guild.id), catch_info["user"], catch_info["pokemon"], catch_info["level"], catch_info["type"], catch_info["streak"])

    # Send to current Channel
    await message.channel.send(embed=reply)

    # Send to Starboard
    starboard_reply = await starboard_helper.send_starboard(str(message.guild.id), catch_info["user"], catch_info["level"], catch_info["pokemon"], message, catch_info["type"], catch_info["streak"])

    # send feedback in the current channel
    await message.channel.send(embed=starboard_reply)

"""check if any message is a rare catch message"""

async def determine_rare_catch(msg):

    message = msg.replace("!", "").replace(".", "").replace("♂️", "").replace("♀️", "") # remove the shit
    message_words = message.split()  

    is_shiny = True
    catch_info = {}     # stores the info of the catch

    catch_keywords = ["Congratulations", "You", "caught", "a", "level"]
    shiny_keywords = ["These", "colors", "seem", "unusual"]

    # determines whether this message is a catch message by checking the presence of the all catch keywords
    for catch_keyword in catch_keywords:
        if catch_keyword not in message_words:
            return None # Not a catch message
    
    # determine shiny catch by checking the presence of all the shiny keywords
    for shiny_keyword in shiny_keywords:
        if shiny_keyword not in message_words:
            is_shiny = False
            break

    # remove the extra text from the message
    extra_text = ["Congratulations", "You caught a level", "+1 Shiny chain!", "Shiny streak reset.", "This is your", "10th", "Added to Pokédex", "You received", "Pokécoins", "These colors seem unusual...", "✨", ".", "!", "(", ")", "*", ","]

    info_text = msg
    for extra in extra_text:
        info_text = info_text.replace(extra, "")

    info_words:list = info_text.split()      # stores the information as values in the list

    catch_streak_text = ["100th", "1000th", "10000th"]

    streak = 0

    if catch_streak_text[0] in info_words:
        streak = 100
        info_words.remove("100th")
    elif catch_streak_text[1] in info_words:
        streak = 1000
        info_words.remove("1000th")
    elif catch_streak_text[2] in info_words:
        streak = 10000
        info_words.remove("10000th")

    catch_info["user"] = ""
    catch_info["level"] = 0
    catch_info["pokemon"] = ""
    catch_info["type"] = ""
    catch_info["streak"] = 0
    
    while info_words[-1].isnumeric():
        info_words.remove(info_words[-1])

    pokemon_name_words = []

    for i in range(len(info_words) -1, -1, -1):
        if info_words[i].isnumeric():
            catch_info["level"] = info_words[i]
            catch_info["user"] = " ".join(info_words[0 : i])
            pokemon_name_words = info_words[i + 1: ]
            break

    # remove duplicates from pokemon_name_words
    unique_pokemon_name_words = []
    for i in pokemon_name_words:
        if i not in unique_pokemon_name_words:
            unique_pokemon_name_words.append(i)

    if is_shiny:
        catch_info["type"] = "shiny"
        catch_info["pokemon"] = " ".join(unique_pokemon_name_words)
        return catch_info
    else:
        catch_info["pokemon"] = " ".join(unique_pokemon_name_words)
        for i in unique_pokemon_name_words:
            try:
                if i.lower() == "galarian" or i.lower() == "alolan" or i.lower() == "hisuian" or cache_manager.cached_rarity_data[i.lower()] in ["legendary", "mythical", "ultra beast"]:
                    catch_info["type"] = "rare"
            except:
                continue

    catch_info["streak"] = streak

    return catch_info
