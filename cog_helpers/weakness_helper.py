import discord

from managers import cache_manager

all_types = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

async def get_weakness_embed(ctx, params):
    params = [p.lower() for p in params]

    # determine the type of input
    type_input = (True if params[0] in all_types else False)

    # return if input error
    if type_input:
        for t in params:
            if t.lower() not in all_types:
                await ctx.send("Input Error, either give a valid type set or a valid pokemon name")
                return
    else:
        if len(params) > 1:
            await ctx.send("Input Error, either give a valid type set or a valid pokemon name")
            return

    # get types from the input
    try:
        if not type_input:
            types = cache_manager.cached_type_data[params[0]]
        else:
            types = params
    except KeyError as err:
        await ctx.send("Pokemon not found")
        return

    # get individual weakness per type
    individual_weakness = {}

    for type in types:
        individual_weakness[type.lower()] = cache_manager.cached_weakness_data[type.lower()]

    # get overall weakness after multiplying the individual weaknesses
    overall_weakness = {"bug": 1, "dark": 1, "dragon": 1, "electric": 1, "fairy": 1, "fighting": 1, "fire": 1, "flying": 1, "ghost": 1, "grass": 1, "ground": 1, "ice": 1, "normal": 1, "poison": 1, "psychic": 1, "rock": 1, "steel": 1, "water": 1}

    for i in list(individual_weakness.keys()):
        for j in all_types:
            overall_weakness[j] = overall_weakness[j] * individual_weakness[i][j]

    # divide the overall weaknesses into tiers
    weakness_tiers = {"super weak" : "", "weak" : "", "neutral" : "", "resistive" : "", "super resistive" : "","immune" : ""}

    for type in list(overall_weakness.keys()):
        if overall_weakness[type] > 2:
            weakness_tiers["super weak"] = weakness_tiers["super weak"] + type.capitalize() + " - "
        elif overall_weakness[type] > 1:
            weakness_tiers["weak"] = weakness_tiers["weak"] + type.capitalize() + " - "
        elif overall_weakness[type] == 1:
            weakness_tiers["neutral"] = weakness_tiers["neutral"] + type.capitalize() + " - "
        elif overall_weakness[type] > 0.5:
            weakness_tiers["resistive"] = weakness_tiers["resistive"] + type.capitalize() + " - "
        elif overall_weakness[type] > 0:
            weakness_tiers["super resistive"] = weakness_tiers["super resistive"] + type.capitalize() + " - "
        else:
            weakness_tiers["immune"] = weakness_tiers["immune"] + type.capitalize() + " - "

    # prepare the embed heading
    heading = ""

    if type_input:
        for i in types:
            heading += f"{i.capitalize()} "
    else:
        heading = f"{params[0].capitalize()} ["
        for i in types:
            heading += f"{i.capitalize()} "
        heading += "]"

    # prepare and send the embed
    embed = discord.Embed(title=f"{heading} weakness details", color=discord.Color.blue())

    for tier in list(weakness_tiers.keys()):
        
        if len(weakness_tiers[tier]) <= 0:
            continue

        embed.add_field(
            name=f"{tier.capitalize()} against",
            value=weakness_tiers[tier],
            inline=False
        )

        if type_input is False:
            embed.set_thumbnail(url=f"https://play.pokemonshowdown.com/sprites/xyani/{params[0].lower()}.gif")

    return embed