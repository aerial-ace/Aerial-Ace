from discord import Embed, Guild

from managers import mongo_manager
from helpers import logger
from config import NORMAL_COLOR

async def set_channel(server_id:int, channel_id:int):

    query = {"server_id" : str(server_id)}

    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                "channel_id" : str(channel_id)
            }
        )

    except Exception as e:
        logger.Logger.logError(e, "Error Occurred while trying to change the donation channel")
        return False
    
    else:
        return True
    
async def set_staff_role(server_id:int, role_id:int):

    query = {"server_id" : str(server_id)}

    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                "staff_role_id" : str(role_id)
            }
        )

    except Exception as e:
        logger.Logger.logError(e, "Error occurred while trying to set staff role id")
        return False

    else:
        return True
    
async def get_donation_leaderboard_embed(server:Guild) -> Embed:

    cursor = await mongo_manager.manager.get_all_data(
        collection_name="donations",
        query={"server_id" : str(server.id)}
    )

    data = cursor[0]
    donations = data.get("donations", {})

    sorted_donations = dict(sorted(donations.items(), key=lambda item: item[1]["value"], reverse=True))

    embd:Embed = Embed(title=f"{server.name}'s Donation Leaderboard", color=NORMAL_COLOR, description="")
    embd.description += "`-#- | Pokecoins | Shiny | Rares | Redeems | Donator `\n\n"

    for pos, donation in enumerate(sorted_donations.items()):
        pokecoins = donation[1].get("pokecoins")
        shinies   = donation[1].get("shinies")
        rares     = donation[1].get("rares")
        redeems   = donation[1].get("redeems")
        user_name = donation[1].get("name")
        user_id   = donation[0]

        embd.description += "`{} | {} | {} | {} | {} |` {} \n".format(f"{pos + 1}".ljust(3, " "), f"{pokecoins}".ljust(9, " "), f"{shinies}".ljust(5, " "), f"{rares}".ljust(5, " "), f"{redeems}".ljust(7, " "), f"[{user_name[:12]}](https://discord.com/users/{user_id})".ljust(9, " "))

    return embd
