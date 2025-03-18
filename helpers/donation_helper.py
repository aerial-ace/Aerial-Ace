from discord import Embed, Guild, Member
import logging

from views.PaginatorViews import PageView
from managers import mongo_manager
from helpers import general_helper
from config import NORMAL_COLOR, WARNING_COLOR


async def get_donation_information_embed(server: Guild) -> Embed:
    cursor = await mongo_manager.manager.get_all_data("donations", {"server_id": str(server.id)})

    data = cursor[0]

    embd = Embed(title=f"{server.name}'s Donation Information", color=NORMAL_COLOR)

    channel_id = data.get("channel_id", None)
    embd.add_field(
        name="Channel",
        value=f"<#{channel_id}>" if channel_id != "0" else "N/A",
        inline=True
    )

    staff_role_id = data.get("staff_role_id", None)
    embd.add_field(
        name="Staff Role",
        value=f"<@&{staff_role_id}>" if staff_role_id != "0" else "N/A",
        inline=True
    )

    log_channel_id = data.get("log_channel_id", None)
    embd.add_field(
        name="Log Channel",
        value=f"<#{log_channel_id}>" if log_channel_id != "0" else "N/A",
        inline=True
    )

    return embd


async def set_channel(server_id: int, channel_id):
    query = {"server_id": str(server_id)}

    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                "channel_id": str(channel_id)
            } if channel_id is not None else {
                "channel_id": "0"
            }
        )

    except Exception as e:
        logging.exception("Error Occurred while trying to change the donation channel")
        return False

    else:
        return True


async def set_staff_role(server_id: int, role_id: int):
    query = {"server_id": str(server_id)}

    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                "staff_role_id": str(role_id)
            }
        )

    except Exception as e:
        logging.exception("Error occurred while trying to set staff role id")
        return False

    else:
        return True


async def get_donation_leaderboard_embed(server: Guild) -> PageView:
    cursor = await mongo_manager.manager.get_all_data(
        collection_name="donations",
        query={"server_id": str(server.id)}
    )

    data = cursor[0]
    donations = data.get("donations", {})

    if len(donations.items()) <= 0:
        return PageView(pages=[Embed(title="Whoops!", description="No Donations Found!", color=WARNING_COLOR)], show_all_btns=False)

    sorted_donations = dict(sorted(donations.items(), key=lambda item: item[1]["value"], reverse=True))

    embd: Embed = Embed(title=f"{server.name}'s Donation Leaderboard", color=NORMAL_COLOR, description="")
    embd.description += "`No. | Pokecoins | Shiny | Rares | Redeems | Donator `\n\n"

    max_number_of_entries_per_embed = 20

    pages: list = []

    donation_items = sorted_donations.items()

    for pos, donation in enumerate(donation_items):

        pokecoins = donation[1].get("pokecoins")
        shinies = donation[1].get("shinies")
        rares = donation[1].get("rares")
        redeems = donation[1].get("redeems")
        user_name = donation[1].get("name")
        user_id = donation[0]

        embd.description += "`{} | {} | {} | {} | {} |` {} \n".format(f"{pos + 1}".ljust(3, " "), f"{pokecoins}".ljust(9, " "), f"{shinies}".ljust(5, " "), f"{rares}".ljust(5, " "), f"{redeems}".ljust(7, " "), f"[{user_name[:12]}](https://discord.com/users/{user_id})".ljust(9, " "))

        if pos + 1 == len(donation_items):
            pages.append(embd)
            break

        if (pos + 1) % max_number_of_entries_per_embed == 0:
            pages.append(embd)

            embd = Embed(title=f"{server.name}'s Donation Leaderboard", color=NORMAL_COLOR, description="")
            embd.description += "`No. | Pokecoins | Shiny | Rares | Redeems | Donator `\n\n"

    paginator = PageView(pages, True)

    return paginator


async def change_donation_values(server: Guild, target: Member, pokecoins: int = 0, shinies: int = 0, rares: int = 0, redeems: int = 0) -> bool:
    query = {"server_id": str(server.id)}

    try:
        value = await general_helper.get_trade_value(pokecoins, shinies, rares, redeems)

        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query=query,
            updated_data={
                f"donations.{target.id}.name": target.name,
                f"donations.{target.id}.pokecoins": pokecoins,
                f"donations.{target.id}.shinies": shinies,
                f"donations.{target.id}.rares": rares,
                f"donations.{target.id}.redeems": redeems,
                f"donations.{target.id}.value": value
            }
        )
    except:
        return False
    else:
        return True


async def set_log_channel(server_id: int, log_channel_id):
    await mongo_manager.manager.update_all_data(
        col_name="donations",
        query={"server_id": str(server_id)},
        updated_data={
            "log_channel_id": str(log_channel_id) if log_channel_id is not None else "0"
        }
    )


async def clear_leaderboard(server_id: int):
    try:
        await mongo_manager.manager.update_all_data(
            col_name="donations",
            query={"server_id": str(server_id)},
            updated_data={
                "donations": {}
            }
        )
    except:
        return False
    else:
        return True


async def remove_user(server_id: int, user_id: int):
    await mongo_manager.manager.remove_entry(
        collection_name="donations",
        query={"server_id": str(server_id)},
        unset_data={
            "donations.{}".format(user_id): ""
        }
    )

    return True
