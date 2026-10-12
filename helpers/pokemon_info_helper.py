import random

import discord

from config import ERROR_COLOR, NON_SHINY_LINK_TEMPLATE, NORMAL_COLOR, TYPES
from helpers import general_helper
from managers import cache_manager
from managers.logging_manager import get_logger

logger = get_logger()


async def get_stats_embed(pokemon):
    # get stats embed

    pokemon = pokemon.lower()
    embd = discord.Embed()

    cached_stats_data = cache_manager.cached_stats_data

    all_pokemon = list(cached_stats_data.keys())
    embd.color = NORMAL_COLOR

    if pokemon in all_pokemon:
        embd.title = f"{pokemon.capitalize()}'s Stats"
        embd.add_field(name="Stats", value=f"```{cached_stats_data[pokemon]}```", inline=False)

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon.lower())
        embd.set_thumbnail(url=image_link)

    else:
        embd.title = "That pokemon was not found in the database"
        embd.color = ERROR_COLOR
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling \n"
        embd.description += "> Stats for **most** mega are same as their non mega forms"

    embd.set_footer(text="This data might be outdated! If you can help with the data update, please reach out in the support server!")
    return embd


async def get_moveset_embed(poke):
    # get moveset embed

    poke = poke.lower()
    embd = discord.Embed()

    cached_moveset_data = cache_manager.cached_moveset_data

    all_pokemon = list(cached_moveset_data.keys())
    embd.color = NORMAL_COLOR

    if poke in all_pokemon:
        embd.title = f"{poke.capitalize()}'s Moveset"
        embd.description = f"```{cached_moveset_data[poke]}```"

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=poke.lower())
        embd.set_thumbnail(url=image_link)

    else:
        embd.title = "That pokemon was not found in the database"
        embd.color = ERROR_COLOR
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling\n"
        embd.description += "> If this pokemon is a mega, try searching their non mega form"

    embd.set_footer(text="This data might be outdated! If you can help with the data update, please reach out in the support server!")
    return embd


async def get_nature_embed(poke: str):
    # get nature embed

    poke = poke.lower()
    embd = discord.Embed()

    try:
        nature = cache_manager.cached_nature_data[poke]
        embd.title = f"{poke.capitalize()}'s nature"
        embd.color = NORMAL_COLOR
        embd.description = f"```{nature}```"

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=poke.lower())
        embd.set_thumbnail(url=image_link)

    except KeyError:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"

        embd.color = ERROR_COLOR

    embd.set_footer(text="This data might be outdated! If you can help with the data update, please reach out in the support server!")

    return embd


async def get_weakness_embed(params) -> discord.Embed:
    # get weakness embed

    params = [p.lower() for p in params]

    # determine the type of input
    type_input = params[0] in TYPES

    # return if input error; first word is type but any of the other words in not type
    if type_input:
        for t in params:
            if t.lower() not in TYPES:
                reply = await general_helper.get_info_embd(title="Breh, whats this?", desc=f"Input Error, either give a valid type set or a valid pokemon name. {t} is not a valid type name", color=ERROR_COLOR)
                return reply

    types: list[str] = []

    # get types from the input
    if not type_input:
        poke_name = "-".join(params)
        poke_data = await cache_manager.search_cached_type_data(poke_name)
        if poke_data is None:
            ref_num = random.getrandbits(64)
            logger.error("Failed to generate weakness data! No Pokemon Type data received!")
            return await general_helper.get_error_embd(title="Not Found Error!", desc="That pokemon was not found, try this ```-aa weak Emolga\n-aa weak palkia-origin```\nReport missing weakness data of any pokemon in the support server", footer=f"Provide this reference number : {ref_num}")

        types = poke_data.get("types", [])
        if len(types) <= 0:
            ref_num = random.getrandbits(64)
            logger.error(f"Failed to get types from pokemon_data! Pokemon Data is {poke_data}, reference number : {ref_num}")
            return await general_helper.get_error_embd("Whoops!", "Failed to get Weakness Data! Maybe check the pokemon name!", f"Provide this reference number : {ref_num}")
    else:
        types = params

    # get individual weakness per type
    individual_weakness = {}

    for type in types:
        individual_weakness[type.lower()] = cache_manager.cached_weakness_data[type.lower()]

    # get overall weakness after multiplying the individual weaknesses
    overall_weakness = {"bug": 1, "dark": 1, "dragon": 1, "electric": 1, "fairy": 1, "fighting": 1, "fire": 1, "flying": 1, "ghost": 1, "grass": 1, "ground": 1, "ice": 1, "normal": 1, "poison": 1, "psychic": 1, "rock": 1, "steel": 1, "water": 1}

    for i in list(individual_weakness.keys()):
        for j in TYPES:
            overall_weakness[j] = overall_weakness[j] * individual_weakness[i][j]

    # divide the overall weaknesses into tiers
    weakness_tiers = {"super weak": "", "weak": "", "neutral": "", "resistive": "", "super resistive": "", "immune": ""}

    for type in list(overall_weakness.keys()):
        if overall_weakness[type] > 2:
            weakness_tiers["super weak"] = weakness_tiers["super weak"] + type.capitalize() + ", "
        elif overall_weakness[type] > 1:
            weakness_tiers["weak"] = weakness_tiers["weak"] + type.capitalize() + ", "
        elif overall_weakness[type] == 1:
            weakness_tiers["neutral"] = weakness_tiers["neutral"] + type.capitalize() + ", "
        elif overall_weakness[type] > 0.5:
            weakness_tiers["resistive"] = weakness_tiers["resistive"] + type.capitalize() + ", "
        elif overall_weakness[type] > 0:
            weakness_tiers["super resistive"] = weakness_tiers["super resistive"] + type.capitalize() + ", "
        else:
            weakness_tiers["immune"] = weakness_tiers["immune"] + type.capitalize() + ", "

    # prepare the embed heading
    heading = ""
    for i in params:
        heading += i.capitalize() + " "

    # prepare and send the embed
    embed = discord.Embed(title=f"{heading} weakness details", color=discord.Color.blue())

    if not type_input:
        type_text = ""
        for i in types:
            type_text += i.capitalize() + " "

        embed.description = f"Types : {type_text}"

    for tier in list(weakness_tiers.keys()):
        if len(weakness_tiers[tier]) <= 0:
            continue

        embed.add_field(name=f"{tier.capitalize()} against", value=weakness_tiers[tier], inline=False)

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=params[0].lower()).replace("-mega-x", "-megax").replace("-mega-y", "-megay").replace("-female", "-f").replace("-male", "")

        if type_input is False:
            embed.set_thumbnail(url=image_link)

    return embed
