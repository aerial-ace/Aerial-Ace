import discord
import datetime

from cog_helpers import starboard_helper
from managers import cache_manager
import config

# detect rare catch message
async def rare_check(message : discord.Message):    
    if str(message.author.id) != config.ADMIN_ID:
        return

    catch_info = await determine_rare_catch(message.content)

    # return if not a rare catch
    if catch_info is None:
        return

    is_shiny = (True if catch_info["type"] == "shiny" else False)

    # get the rare catch details
    if is_shiny:
        reply = await get_rare_catch_embd(message, catch_info["user"], catch_info["pokemon"], catch_info["level"], True)
    else:
        reply = await get_rare_catch_embd(message, catch_info["user"], catch_info["pokemon"], catch_info["level"], False)

    # Send to current Channel
    await message.channel.send(embed=reply)

    # Send to Starboard
    await starboard_helper.send_starboard(str(message.guild.id), catch_info["user"], catch_info["level"], catch_info["pokemon"], message, is_shiny)

# check if any message is a rare catch message
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
    extra_text = ["Congratulations", "You caught a level", "+1 Shiny chain!", "Shiny streak reset.", "This is your", "10th", "100th", "1000th", "Added to Pokédex", "You received", "Pokécoins", "These colors seem unusual...", "✨", ".", "!", "(", ")", "*", ","]

    info_text = msg
    for extra in extra_text:
        info_text = info_text.replace(extra, "")

    info_words = info_text.split()      # stores the inforamation as values in the list

    catch_info["user"] = ""
    catch_info["level"] = 0
    catch_info["pokemon"] = ""
    catch_info["type"] = ""
    
    while info_words[-1].isnumeric():
        info_words.remove(info_words[-1])

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
                if i.lower() == "galarian" or i.lower() == "alolan" or cache_manager.cached_rarity_data[i.lower()] in ["legendary", "mythical", "ultra beast"]:
                    catch_info["type"] = "rare"
            except:
                continue

    if catch_info["type"] == "":
        return None

    return catch_info

# returns the embed containing the rare catch info
async def get_rare_catch_embd(_message, _ping, _pokemon, _level, is_shiny:bool):

    embd = discord.Embed(colour=config.RARE_CATCH_COLOR)

    if is_shiny is not True:
        embd.title = ":star2: Rare Catch Detected :star2:"
        embd.description = f"{_ping} caught a level {_level} `{_pokemon.strip()}`\n"
        embd.set_image(url=config.JIRACHI_WOW)
    else:
        embd.title = ":star2: Shiny Catch Detected :star2:"
        embd.description = f"{_ping} caught a level {_level} **SHINY** `{_pokemon}`\n"
        embd.set_image(url=config.PIKA_SHOCK)

    embd.description += f"Congratulations :tada: :tada:\n"

    # set the time of the catch 
    _date = datetime.date.today().strftime("%d %b %y")
    _time_object = datetime.datetime.now(datetime.timezone.utc)
    _time = _time_object.strftime("%I:%M %p UTC")

    embd.set_footer(text=f"{_date} at {_time}")

    return embd