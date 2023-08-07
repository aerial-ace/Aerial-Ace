from discord import AutoShardedBot, Member
from discord import Message

from managers import mongo_manager
from managers import cache_manager
from helpers import general_helper
from config import POKETWO_ID, TRADE_ITEM_WEIGHT

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

    server_data_cursor = await mongo_manager.manager.get_all_data("servers", {"server_id" : str(message.guild.id)})

    if server_data_cursor[0].get("tier", 0) < minimum_required_tier:
        return

    data_cursor = await mongo_manager.manager.get_all_data("donations", {"server_id" : str(message.guild.id)})

    staff_role_id = int(data_cursor[0].get("staff_role_id", 0))

    donator = None
    staff = None

    first_member = message.author
    second_member = None

    for mention in message.mentions:
        if mention.bot is False:
            second_member = mention
            break

    for role in second_member.roles:
        if role.id == staff_role_id:
            staff = second_member
            donator = first_member
            break

    if staff is None:
        for role in first_member.roles:
            if role.id == staff_role_id:
                staff = first_member
                donator = second_member
                break

    if staff is None:
        return await message.channel.send("No Donation Staff is involved in this trade! No logs will be recorded!")

    def wait_for_trade_initiation(message:Message):
        
        if message.author.id != int(POKETWO_ID):
            return False

        if len(message.embeds) <= 0:
            return False

        embd = message.embeds[0]

        if "Trade between" not in embd.title or donator.display_name not in embd.title or staff.display_name not in embd.title:
            return False

        return True

    try:
        await bot.wait_for("message", check=wait_for_trade_initiation, timeout=60)
    except:
        return await message.channel.send("> No response from Poketwo Recieved, Donation Log session cancelled!")
    else:
        await message.channel.send("> Donation Log Session Started! This donation will be logged automatically on completion!\n**NOTE** : Please don't add more than 20 items (1 page) at a time.")

    pokecoins = 0
    rares     = 0
    shinies   = 0
    redeems   = 0

    def wait_for_trade_completion(message:Message):

        nonlocal pokecoins, rares, shinies, redeems

        if message.author.id != int(POKETWO_ID):
            return False
        
        if len(message.embeds) <= 0:
            return False
        
        embd = message.embeds[0]

        if "Completed trade between" not in embd.title or donator.display_name not in embd.title or staff.display_name not in embd.title:
            return False
        
        donator_field = [field for field in embd.fields if donator.display_name in field.name]

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

        return True

    try:
        await bot.wait_for("message", check=wait_for_trade_completion, timeout=360)
    except TimeoutError as e:
        return await message.channel.send("> Donation Logging Session Timed Out!")
    else:

        await log_donation(message.guild.id, donator.id, pokecoins, rares, shinies, redeems)

        await message.channel.send("Donation has been logged!")
        
async def log_donation(server_id:int, donator:Member, pokecoins:int=0, rares:int=0, shinies:int=0, redeems:int=0):

    cursor = await mongo_manager.manager.get_all_data(
        collection_name="donations",
        query={"server_id" : str(server_id)}
    )

    data = cursor[0]

    donations = data.get("donations", None)

    """
    donations : {
        "348239489238473298" : {
        
            "name"      : "Dev",
            "pokecoins" : 23942042,
            "shinies"   : 23,
            "rares"     : 199,
            "redeems"   : 25,
            "value"     : 0
        }
    ]
    """

    # Calculate the approximate pokecoin value of all items
    value = await general_helper.get_trade_value(pokecoins, shinies, rares, redeems)

    user_donations = donations.get(str(donator.id), {})

    user_donations["name"] = donator.name
    user_donations["shinies"] = user_donations.get("shinies", 0) + shinies
    user_donations["rares"] = user_donations.get("rares", 0) + rares
    user_donations["pokecoins"] = user_donations.get("pokecoins", 0) + pokecoins
    user_donations["redeems"] = user_donations.get("redeems", 0) + redeems
    user_donations["value"] = value

    donations[str(donator.id)] = user_donations

    await mongo_manager.manager.update_all_data(
        col_name="donations",
        query={"server_id" : str(server_id)},
        updated_data={"donations" : donations}
    )