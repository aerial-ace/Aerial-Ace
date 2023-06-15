import discord
import random

from managers import cache_manager, mongo_manager
from helpers import starboard_helper, general_helper
import config

"""detect rare catch message"""

async def rare_check(bot:discord.AutoShardedBot, message : discord.Message):    

    bot_member:discord.Member = message.guild.get_member(bot.user.id)

    if message.channel.permissions_for(bot_member).send_messages is False:
        return

    if str(message.author.id) != config.POKETWO_ID:
        return

    catch_info = await determine_rare_catch(message.content)

    # return if not a rare catch
    if catch_info is None or (catch_info["type"] == "" and catch_info["streak"] == 0):
        return None

    server_details = await mongo_manager.manager.get_all_data("servers", {
        "server_id" : str(message.guild.id)
    })

    # get the rare catch details
    reply = await starboard_helper.get_rare_catch_embd(server_details, catch_info["user"], catch_info["pokemon"], catch_info["level"], catch_info["type"], catch_info["streak"], catch_info["hunt"])

    if reply is None:
        return

    # send the rare catch alert in the current channel
    try:    
        await message.channel.send(embed=reply)
    except discord.errors.Forbidden:
        return # return if not allowed to send messages in the current channel

    customization_reminder_possibility = 30

    if server_details[0].get("tier") == 0 and random.randint(0, 99) < customization_reminder_possibility:

        embd = await general_helper.get_info_embd(f"{config.AERIAL_ACE_EMOJI} Customize Starboard Embed!", "Enhance the starboard embed using various customization features available to premium servers. Get premium now and customize your starboard embeds to suit your servers. ", config.DEFAULT_COLOR, "Use -aa premium or join support server to know more.")

        await message.channel.send(embed=embd)

    # Send to Starboard
    starboard_reply = await starboard_helper.send_starboard(server_details, catch_info["user"], catch_info["level"], catch_info["pokemon"], message, catch_info["type"], catch_info["streak"], catch_info["hunt"])

    # send feedback in the current channel
    await message.channel.send(embed=starboard_reply)

"""check if any message is a rare catch message"""

async def determine_rare_catch(msg):

    message = msg.replace("!", "").replace(".", "").replace("♂️", "").replace("♀️", "") # remove the shit
    message_words = message.split()  

    is_shiny = True
    is_hunt = False
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

    hunt_keywords = ["+1 Shiny chain!", "Shiny streak reset."]
    extra_text = ["Congratulations", "You caught a level", "This is your", "10th", "Added to Pokédex", "You received", "Pokécoins", "These colors seem unusual...", "✨", ".", "!", "(", ")", "*", ","]

    info_text = msg

    for hunt_keyword in hunt_keywords:
        if hunt_keyword in info_text:
            is_hunt = True 
            info_text = info_text.replace(hunt_keyword, "")

    for extra in extra_text:
        info_text = info_text.replace(extra, "")

    # stores the information as values in the list
    info_words:list = info_text.split()     

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
    catch_info["hunt"] = is_hunt
    
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
