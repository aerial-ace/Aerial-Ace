import requests
from discord import Embed
import json

from config import SMOGON_API_TEMPLATE, SMOGON_COLOR, ERROR_COLOR, NON_SHINY_LINK_TEMPLATE
from cog_helpers import general_helper

class SmogonData:

    name:str = ""
    gen:int = 0
    tier:str = ""
    rank:str = ""
    usage:float = 0.0
    abilities:dict = {}
    stats:dict = {}
    moveset:dict = {}
    items:dict = {}
    checks:dict = {}

    error = None
    message = None

async def get_smogon_data(gen:int, tier:str, pokemon:str) -> SmogonData:
    
    smogon_url = SMOGON_API_TEMPLATE.format(gen=gen, tier=tier, pokemon=pokemon)
    smogon_request = requests.get(url=smogon_url)

    data = json.loads(smogon_request.text)

    smogon_data = SmogonData()

    try:
        smogon_data.name = data["pokemon"]
        smogon_data.gen = gen
        smogon_data.tier = tier
        smogon_data.rank = data["rank"]
        smogon_data.usage = data["usage"]
        smogon_data.abilities = data["abilities"]
        smogon_data.moveset = data["moves"]
        smogon_data.items = data["items"]
        smogon_data.checks = data["checks"]
        smogon_data.stats = data["spreads"]
    except:
        try:
            smogon_data.error = data["error"]
            smogon_data.message = data["message"]

            return smogon_data
        except:
            return None

    return smogon_data


async def get_smogon_embed(data:SmogonData) -> Embed:

    if data.error is not None:
        return await general_helper.get_info_embd("Error!!", "**Error Code :** {code}\n**Error Description** {desc}\n\nThere is a possiblity that the searched pokemon is not available in that generation or in that tier. \nTry with gen it was first introduced in.".format(code=data.error, desc=data.message), color=ERROR_COLOR)

    embd = Embed(title=f"{data.name.capitalize()} - Smogon Analysis", color=SMOGON_COLOR)

    embd.add_field(
        name="Gen - Tier",
        value="{} - {}".format(data.gen, data.tier.upper()),
        inline=True
    )
    embd.add_field(
        name="Pokemon",
        value=data.name.capitalize(),
        inline=True
    )
    embd.add_field(
        name="Tier Rank",
        value=data.rank,
        inline=True
    )
    embd.add_field(
        name="Usage Percentage",
        value=data.usage,
        inline=False
    )

    # abilities

    abilities_str = ""
    abilities = list(data.abilities.keys())
    ability_perc = list(data.abilities.values())

    if abilities != {}:
        for i in range(len(abilities)):
            abilities_str += "{} - *{}*\n".format(abilities[i].capitalize(), ability_perc[i])
    else:
        abilities_str = "*Not enough data here*"

    embd.add_field(
        name="Abilities - %",
        value=abilities_str,
        inline=False
    )

    # items

    items_str = ""
    items = list(data.items.keys())
    items_perc = list(data.items.values())

    if items != {}:
        for i in range(len(items)):
            items_str += "{} - *{}*\n".format(items[i].capitalize(), items_perc[i])
    else:
        items_str = "*Not enough data here*"

    embd.add_field(
        name="Items - %",
        value=items_str,
        inline=True
    )

    # moves

    moves_str = ""
    moves = list(data.moveset.keys())
    moves_perc = list(data.moveset.values())

    if moves != []:
        for i in range(len(moves)):
            moves_str += "{} - *{}*\n".format(moves[i].capitalize(), moves_perc[i])
    else:
        moves_str = "*Not enough data here*"

    embd.add_field(
        name="Moves - %",
        value=moves_str,
        inline=True
    )

    # Checks

    checks_str = ""
    checks = list(data.checks.keys())
    checks_perc = list(data.checks.values())

    if checks != []:
        for i in range(len(checks)):
            checks_str += "{} - *{}*\n".format(checks[i].capitalize(), checks_perc[i]["ko"])
    else:
        checks_str = "*Not enough data here*"

    embd.add_field(
        name="Checks - KO%",
        value=checks_str,
        inline=True
    )

    # stats

    stats_str = ""
    natures = list(data.stats.keys())
    all_spreads = list(data.stats.values())

    if natures != []:
        for i in range(len(natures)):
            if natures[i] == "Other":
                spreads = {}
                perc = all_spreads[i]
            else:
                spreads = list(all_spreads[i].keys())
                perc = list(all_spreads[i].values())

            if spreads != {}:
                for j in range(len(spreads)):
                    stats_str += "{} : {} - *{}*\n".format(natures[i], spreads[j], perc[j])
            else:
                stats_str += "Others : *{}*".format(perc)
    else:
        stats_str = "*Not enough data here*"

    embd.add_field(
        name="Stats Spreads - %",
        value=stats_str,
        inline=False
    )
    
    embd.set_image(url=NON_SHINY_LINK_TEMPLATE.format(pokemon=data.name.lower()))
    
    return embd