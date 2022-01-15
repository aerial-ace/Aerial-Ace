import discord

import config
from cog_helpers import general_helper
from managers import cache_manager

async def get_stats_embed(pokemon):
    embd = discord.Embed()

    cached_stats_data = cache_manager.cached_stats_data

    all_pokemon = list(cached_stats_data.keys())
    embd.colour = config.NORMAL_COLOR

    if pokemon in all_pokemon:
        embd.title = "{poke}'s Stats".format(poke=pokemon.capitalize())
        embd.description = "HP, Defense, Sp.Defense and Speed are `The more the better` stats \n"
        embd.add_field(name="Stats", value="```{stats}```".format(stats=cached_stats_data[pokemon]), inline=False)

        return embd

    else:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"
        return embd

async def get_moveset_embed(poke):
    embd = discord.Embed()

    cached_moveset_data = cache_manager.cached_moveset_data

    all_pokemon = list(cached_moveset_data.keys())
    embd.colour = config.NORMAL_COLOR

    if poke in all_pokemon:
        embd.title = "{poke}'s moveset".format(poke=poke.capitalize())
        embd.description = "```{ms}```".format(ms=cached_moveset_data[poke])
        return embd
    else:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"
        return embd

# get nature 
async def get_nature_embed(poke: str):
    embd = discord.Embed()

    try:
        nature = cache_manager.cached_nature_data[poke]
        embd.title = "{poke}'s nature".format(poke=poke.capitalize())
        embd.description = f"```{nature}```"
        embd.color = config.NORMAL_COLOR
    except:
        embd.title = "That pokemon was not found in the database"
        embd.description = "> If the name is correct then \n"
        embd.description += "> PROBABLY this pokemon is not good for battling"
        embd.color = config.ERROR_COLOR
    
    return embds

# return tierlist
async def get_tl(list_name):
    if list_name == "rare":
        return config.RARE_TL
    elif list_name == "mega":
        return config.MEGA_TL
    elif list_name == "common":
        return config.COMMON_TL
    elif list_name == "normal":
        return config.NORMAL_TL
    elif list_name == "fire":
        return config.FIRE_TL
    elif list_name == "water":
        return config.WATER_TL
    elif list_name == "grass":
        return config.GRASS_TL
    elif list_name == "electric":
        return config.ELECTRIC_TL
    elif list_name == "psychic":
        return config.PSYCHIC_TL
    elif list_name == "rock":
        return config.ROCK_TL
    elif list_name == "ground":
        return config.GROUND_TL
    elif list_name == "fighting":
        return config.FIGHTING_TL
    elif list_name == "ghost":
        return config.GHOST_TL
    elif list_name == "dark":
        return config.DARK_TL
    elif list_name == "ice":
        return config.ICE_TL
    elif list_name == "fairy":
        return config.FAIRY_TL
    elif list_name == "dragon":
        return config.DRAGON_TL
    elif list_name == "steel":
        return config.STEEL_TL
    elif list_name == "flying":
        return config.FLYING_TL
    elif list_name == "poison":
        return config.POISON_TL
    elif list_name == "bug":
        return config.BUG_TL
    else:
        return """> That tierlist was not found, these tierlists are available```rare | mega | common | steel```"""