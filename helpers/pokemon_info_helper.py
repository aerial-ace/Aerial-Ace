import discord

from managers import cache_manager
from helpers import general_helper
from config import TYPES, NON_SHINY_LINK_TEMPLATE, NORMAL_COLOR, ERROR_COLOR


# get stats
async def get_stats_embed(pokemon):
    pokemon = pokemon.lower()
    embd = discord.Embed()

    cached_stats_data = cache_manager.cached_stats_data

    all_pokemon = list(cached_stats_data.keys())
    embd.color = NORMAL_COLOR

    if pokemon in all_pokemon:
        embd.title = "{poke}'s Stats".format(poke=pokemon.capitalize())
        embd.add_field(name="Stats", value="```{stats}```".format(stats=cached_stats_data[pokemon]), inline=False)

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=pokemon.lower())
        embd.set_thumbnail(url=image_link)

        embd.set_footer(text="Missing stats for a potentially good pokemon? Report it at official server.")

        return embd

    else:
        embd.title = "That pokemon was not found in the database"
        embd.color = ERROR_COLOR
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling \n"
        embd.description += "> Stats for **most** mega are same as their non mega forms"

        embd.set_footer(text="Missing stats for a potentially good pokemon? Report it at official server")

        return embd


# get moveset
async def get_moveset_embed(poke):
    poke = poke.lower()
    embd = discord.Embed()

    cached_moveset_data = cache_manager.cached_moveset_data

    all_pokemon = list(cached_moveset_data.keys())
    embd.color = NORMAL_COLOR

    if poke in all_pokemon:
        embd.title = "{poke}'s Moveset".format(poke=poke.capitalize())
        embd.description = "```{ms}```".format(ms=cached_moveset_data[poke])

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=poke.lower())
        embd.set_thumbnail(url=image_link)

        embd.set_footer(text="Missing moveset for a potentially good pokemon? Report it at official server.")

        return embd
    else:
        embd.title = "That pokemon was not found in the database"
        embd.color = ERROR_COLOR
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling\n"
        embd.description += "> If this pokemon is a mega, try searching their non mega form"

        embd.set_footer(text="Missing moveset for a potentially good pokemon? Report it at official server.")

        return embd


# get nature
async def get_nature_embed(poke: str):
    poke = poke.lower()
    embd = discord.Embed()

    try:
        nature = cache_manager.cached_nature_data[poke]
        embd.title = "{poke}'s nature".format(poke=poke.capitalize())
        embd.color = NORMAL_COLOR
        embd.description = f"```{nature}```"

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=poke.lower())
        embd.set_thumbnail(url=image_link)

        embd.set_footer(text="Missing nature for a potentially good pokemon? Report it at official server.")
    except KeyError:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"

        embd.set_footer(text="Missing nature for a potentially good pokemon? Report it at official server.")

        embd.color = ERROR_COLOR

    return embd


# get weakness
async def get_weakness_embed(params):
    params = [p.lower() for p in params]

    # determine the type of input
    type_input = (True if params[0] in TYPES else False)

    # return if input error
    if type_input:
        for t in params:
            if t.lower() not in TYPES:
                reply = await general_helper.get_info_embd(title="Breh, whats this?", desc="Input Error, either give a valid type set or a valid pokemon name", color=ERROR_COLOR)
                return reply
    else:
        if len(params) > 1:
            reply = await general_helper.get_info_embd(title="Breh, whats this?", desc="Input Error, either give a valid type set or a valid pokemon name", color=ERROR_COLOR)
            return reply

    # get types from the input
    try:
        if not type_input:
            types = (await cache_manager.search_cached_type_data(params[0]))["types"]
        else:
            types = params
    except KeyError as err:
        return await general_helper.get_info_embd(title="Not Found Error!", desc="That pokemon was not found, try this ```-aa weak Emolga```", color=ERROR_COLOR, footer="Report missing weakness data of any pokemon at the official server when?")

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

        embed.add_field(
            name=f"{tier.capitalize()} against",
            value=weakness_tiers[tier],
            inline=False
        )

        image_link = NON_SHINY_LINK_TEMPLATE.format(pokemon=params[0].lower()).replace("-mega-x", "-megax").replace("-mega-y", "-megay").replace("-female", "-f").replace("-male", "")

        if type_input is False:
            embed.set_thumbnail(url=image_link)

    return embed
