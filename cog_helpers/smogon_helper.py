import requests
from discord import Embed
import json

from config import SMOGON_API_TEMPLATE, SMOGON_COLOR

class SmogonData:

    name:str = ""
    tier:str = ""
    rank:str = ""
    usage:float = 0.0
    abilities:dict = {}
    stats:dict = {}
    moveset:dict = {}
    checks:dict = {}


async def get_smogon_data(tier:str, pokemon:str) -> SmogonData:
    
    smogon_url = SMOGON_API_TEMPLATE.format(tier=tier, pokemon=pokemon)
    smogon_request = requests.get(url=smogon_url)

    data = json.loads(smogon_request.text)

    smogon_data = SmogonData()

    smogon_data.name = data["pokemon"]
    smogon_data.tier = data["tier"]
    smogon_data.rank = data["rank"]
    smogon_data.usage = data["usage"]
    smogon_data.abilities = data["abilities"]
    smogon_data.moveset = data["moves"]
    smogon_data.checks = data["checks"]

    return smogon_data


async def get_smogon_embed(data:SmogonData) -> Embed:

    print(data)

    embd = Embed(title=f"{data.name.capitalize()} - Smogon Analysis", color=SMOGON_COLOR)

    embd.description = "**Tier :** {}".format(data.tier.capitalize()) + "\n"
    embd.description += "**Pokemon :** {}".format(data.name.capitalize()) + "\n"
    embd.description += "**Tier Ranking :** {}".format(data.rank) + "\n"
    embd.description += "**Tier Usage :** in {} of all teams".format(data.usage)
    
    return embd