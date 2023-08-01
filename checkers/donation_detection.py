from discord import AutoShardedBot, Member
from discord import Message

from managers import mongo_manager
from helpers.logger import Logger
from managers import cache_manager
from config import POKETWO_ID

async def donation_check(bot:AutoShardedBot, message:Message):

    bot_member:Member = message.guild.get_member(bot.user.id)

    # Return if not allowed to send messages
    if message.channel.permissions_for(bot_member).send_messages is False:
        return

    content = message.content.strip()

    # Return if not a poketwo command
    if content.startswith(f"<@{POKETWO_ID}"):
        content = message.content.removeprefix(f"<@{POKETWO_ID}")
    else:
        return
    
    if content.strip().endswith(">") is False:
        return
    
    content = content.replace("<@", "").replace(">", "").replace("&", "")

    # Check if the message is a trade command
    trade_initiation_keywords = ["trade", "t"]

    for keyword in trade_initiation_keywords:
        if keyword in content:
            content = content.replace(keyword, "")
            break
    else:
        return  
    
    # check whether this server is premium or not
    minimum_required_tier = 2

    data_cursor = await mongo_manager.manager.get_all_data("servers", {"server_id" : str(message.guild.id)})

    if data_cursor[0].get("tier", 0) < minimum_required_tier:
        return

    donator_id = message.author.id
    donator_name = message.author.display_name

    staff = None

    for mention in message.mentions:
        if mention.bot is False:
            staff = mention

    Logger.logMessage("Donator Name : " + donator_name)
    Logger.logMessage("Donator ID : " + str(donator_id))
    Logger.logMessage("Staff Name : " + staff.display_name)
    Logger.logMessage("Staff ID : " + str(staff.id))

    def wait_for_trade_initiation(message:Message):
        
        if message.author.id != int(POKETWO_ID):
            return False

        if len(message.embeds) <= 0:
            return False

        embd = message.embeds[0]

        if "Trade between" not in embd.title or donator_name not in embd.title or staff.display_name not in embd.title:
            return False

        return True

    try:
        await bot.wait_for("message", check=wait_for_trade_initiation, timeout=60)
    except TimeoutError as t:
        return await message.channel.send("> No response from Poketwo Recieved, Donation Log session cancelled!")
    else:
        await message.channel.send("> Donation Log Session Started! This donation will be logged automatically on completion!")

    def wait_for_trade_completion(message:Message):

        if message.author.id != int(POKETWO_ID):
            return False
        
        if len(message.embeds) <= 0:
            return False
        
        embd = message.embeds[0]

        if "Completed trade between" not in embd.title or donator_name not in embd.title or staff.display_name not in embd.title:
            return False
        
        donator_field = [field for field in embd.fields if donator_name in field.name]

        pokecoins = 0
        rares     = 0
        shinies   = 0
        redeems   = 0

        field_lines = donator_field[0].value.split("\n")

        for line in field_lines:
            if line.endswith("Pokécoins"):
                pokecoins = pokecoins + int(line.split()[0].replace(",", ""))

            elif line.endswith("redeems"):
                redeems = redeems + int(line.split()[0])

            elif "✨" in line:
                shinies = shinies + 1

            else:
                first_split = line.split("•")[0]

                first_split = first_split.replace("*", "").replace("`", "")

                pokemon = first_split.split()[-1].lower()

                if cache_manager.cached_rarity_data.get(pokemon, "common") in ["legendary", "mythical", "ultra beast"]:
                    rares = rares + 1

        print(pokecoins)
        print(rares)
        print(shinies)
        print(redeems)

        return True

    try:
        await bot.wait_for("message", check=wait_for_trade_completion, timeout=360)
    except TimeoutError as e:
        return await message.channel.send("> Donation Logging Session Timed Out!")
    else:
        await message.channel.send("Donation has been logged!")


    


        
