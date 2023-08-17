from discord import AutoShardedBot, Member, Forbidden
from discord import Message, TextChannel, Embed

from managers import mongo_manager
from managers import cache_manager
from helpers import general_helper
from config import POKETWO_ID, NORMAL_COLOR, INFO_EMOJI

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

    conclusion_type = None

    def wait_for_cancellation(message:Message):

        nonlocal conclusion_type

        if not message.content.strip().startswith(f"<@{POKETWO_ID}>"):
            return False
        
        if "x" not in message.content.lower() and "cancel" not in message.content.lower():
            return False 

        battle_cancel_keywords = ["trade ", "t "]
        
        for keyword in battle_cancel_keywords:
            if keyword in message.content:
                break
        else:
            return False

        conclusion_type = "CANCELLED"

        return True
    
    def wait_for_completion(message:Message):

        nonlocal pokecoins, rares, shinies, redeems, conclusion_type

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

        conclusion_type = "COMPLETED"

        return True

    def wait_for_conclusion(message:Message):

        if wait_for_cancellation(message) is not False:
            return True
        
        if wait_for_completion(message) is not False:
            return True
        
        return False

    try:
        trade_complete_message = await bot.wait_for("message", check=wait_for_conclusion, timeout=360)

    except TimeoutError as e:
        return await message.channel.send("> Donation Logging Session Timed Out!")

    else:
        if conclusion_type == "CANCELLED":
            return await message.channel.send("Session Cancelled!")

        await log_donation(message.guild.id, donator, pokecoins, rares, shinies, redeems, data_cursor)

        log_channel_id = data_cursor[0].get("log_channel_id")

        # Only log if log channel is provided!
        if log_channel_id == "0":
            return

        log_channel:TextChannel = message.guild.get_channel(int(log_channel_id))

        log_embd = Embed(title="Donation Log", color=NORMAL_COLOR)

        log_embd.add_field(
            name="Donator",
            value=donator.mention,
            inline=True
        )

        log_embd.add_field(
            name="Staff Involved",
            value=staff.mention,
            inline=True
        )

        log_embd.add_field(
            name="Status",
            value=f"{INFO_EMOJI} Not Collected",
            inline=False
        )

        log_embd.add_field(
            name="Teleport",
            value="[Click Here]({})".format(trade_complete_message.jump_url),
            inline=True
        )

        donated_items_str = "```Pokecoins : {}\nShinies : {}\nRares : {}\nRedeems : {}```".format(pokecoins, shinies, rares, redeems)

        log_embd.add_field(
            name="Items Donated",
            value=donated_items_str,
            inline=False
        )

        log_embd.set_thumbnail(url=donator.avatar.url)

        try:
            await log_channel.send(embed=log_embd)
        except Forbidden:
            return await message.channel.send("Not Allowed to send messages in {}! Please Check Permissions".format(log_channel.mention))

        await message.channel.send("Donation has been logged!")
        
async def log_donation(server_id:int, donator:Member, pokecoins:int=0, rares:int=0, shinies:int=0, redeems:int=0, data_cursor=None):

    if data_cursor is None:
        data_cursor = await mongo_manager.manager.get_all_data(
            collection_name="donations",
            query={"server_id" : str(server_id)}
        )

    data = data_cursor[0]

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

    user_donations     = donations.get(str(donator.id), {})

    new_pokecoin_count = user_donations.get("pokecoins", 0) + pokecoins
    new_shiny_count    = user_donations.get("shinies", 0) + shinies
    new_rare_count     = user_donations.get("rares", 0) + rares
    new_redeem_count   = user_donations.get("redeems", 0) + redeems

    # Calculate the approximate pokecoin value of all items
    value = await general_helper.get_trade_value(new_pokecoin_count, new_shiny_count, new_rare_count, new_redeem_count)

    user_donations["name"] = donator.name
    user_donations["shinies"] = new_shiny_count
    user_donations["rares"] = new_rare_count
    user_donations["pokecoins"] = new_pokecoin_count
    user_donations["redeems"] = new_redeem_count
    user_donations["value"] = value

    donations[str(donator.id)] = user_donations

    await mongo_manager.manager.update_all_data(
        col_name="donations",
        query={"server_id" : str(server_id)},
        updated_data={"donations" : donations}
    )