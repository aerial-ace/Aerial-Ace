import random
import requests
import json
from textwrap import TextWrapper
import global_vars
import aerialace_data_manager


class PokeData:

    p_id = 0
    p_name = ""
    p_types = ""
    p_region = ""
    p_abilities = ""
    p_weight = 0.0
    p_height = 0.0
    image_link = ""
    p_info = ""
    p_stats = {}

# for getting the help embed


def get_help_embed(embd, color):
    embd.title = "Aerial Ace Help"
    embd.color = color

    # help fields
    embd.add_field(name="Say Hello",
                   value="`-aa Hello` `-aa Hola`", inline=False)
    embd.add_field(
        name="Rolling", value="`-aa roll` `-aa roll <upper limit>`", inline=False)
    embd.add_field(name="Random Pokemon",
                   value="`-aa rp` `-aa rand_poke`", inline=False)
    embd.add_field(name="View Dex Entry",
                   value="`-aa dex <pokedex id>` `-aa dex <pokemon name>`", inline=False)
    embd.add_field(name="Set Favourite Pokemon",
                   value="`-aa set_fav <pokemon name>`", inline=False)
    embd.add_field(name="View Favourite Pokemon",
                   value="`-aa fav`", inline=False)
    embd.add_field(
        name="Stats", value="`-aa stats <Pokemon Name>`", inline=False)
    embd.add_field(name="Tierlists",
                   value="`-aa tl <tierlist type>`", inline=False)
    embd.add_field(name="Stats Check",
                   value="`-aa stats <pokemon>`", inline=False)
    embd.add_field(name="Moveset Check",
                   value="`-aa ms <pokemon>`", inline=False)

    return embd

# for getting a pokemon of desired index


def get_poke_by_id(id):

    poke = PokeData()

    general_response = requests.get(
        "https://pokeapi.co/api/v2/pokemon/{0}".format(id))
    data = json.loads(general_response.text)

    species_response = requests.get(
        "https://pokeapi.co/api/v2/pokemon-species/{0}/".format(id))
    species_data = json.loads(species_response.text)

    generation_response = requests.get(
        "https://pokeapi.co/api/v2/generation/{name}/".format(name=species_data["generation"]["name"]))
    generation_data = json.loads(generation_response.text)

    poke.p_id = data["id"]

    # get name
    poke.p_name = data["name"].capitalize()

    # get height and weight
    poke.p_height = float(data["height"])
    poke.p_weight = float(data["weight"])

    # get types
    types = data["types"]

    for i in range(0, len(types)):
        poke.p_types += types[i]["type"]["name"].capitalize()

        if i != len(types) - 1:
            poke.p_types += ' | '

    # get_region
    poke.p_region = generation_data["main_region"]["name"].capitalize()

    # get abilities
    abilities = data["abilities"]

    for i in range(0, len(abilities)):
        poke.p_abilities += abilities[i]["ability"]["name"].capitalize()

        if i != len(abilities) - 1:
            poke.p_abilities += ' | '

    # get info
    allInfos = species_data["flavor_text_entries"]
    poke.p_info = "*NULL*"

    for i in allInfos:
        if i["language"]["name"] == "en":
            poke.p_info = i["flavor_text"]
            break

    # get image_link
    poke.image_link = data["sprites"]["front_default"]

    # get stats
    stats = data["stats"]

    for i in range(0, len(stats)):
        stat_name = stats[i]["stat"]["name"]
        stat_value = stats[i]["base_stat"]
        poke.p_stats[stat_name] = stat_value

    return poke

# for getting a random pokemon


def get_random_poke():

    rand_pokemon_id = random.randint(1, 898)

    poke = get_poke_by_id(rand_pokemon_id)

    return poke

# for wraping text


def wrap_text(width, text):
    wrapped_text = ""
    wrapper = TextWrapper(width)
    text_lines = wrapper.wrap(text)
    for line in text_lines:
        wrapped_text += "{line}\n".format(line=line)

    return wrapped_text

# rolling


def roll(max):
    roll = random.randint(0, max)
    return roll

# get parameter from the message


def get_parameter(msg, removable_command):
    param = msg
    for cmd in removable_command:
        param = param.replace(cmd, "").strip()

    return param

# get random pokemon embed


def get_random_pokemon_embed(embd, pokeData, color, server_id, user_id):

    embd.color = color
    embd.title = "**{0} : {1}**".format(pokeData.p_id, pokeData.p_name)

    description = wrap_text(40, pokeData.p_info)
    embd.description = description
    embd.set_image(url=pokeData.image_link)

    # Ugly, ik '_'
    fav_poke = ""
    fav_out = aerialace_data_manager.get_fav(server_id, user_id)
    if fav_out.startswith("> Your favourite pokemon is"):
        fav_poke = fav_out.replace(
            "> Your favourite pokemon is", "").strip().lower().replace("*", "")
        if pokeData.p_name.lower() == fav_poke:
            embd.set_footer(text="This pokemon is your favourite")

    return embd

# get Dex entry embed


def get_dex_entry_embed(embd, pokeData, color):
    embd.color = color
    embd.title = "**{0} : {1}**".format(pokeData.p_id, pokeData.p_name)

    description = wrap_text(40, pokeData.p_info)
    description += "\n"

    embd.add_field(name="Height", value="{h} m".format(
        h=pokeData.p_height), inline=True)
    embd.add_field(name="Weight", value="{w} kg".format(
        w=pokeData.p_weight), inline=True)
    embd.add_field(name="Region", value="{r}".format(
        r=pokeData.p_region), inline=True)
    embd.add_field(name="Type(s)", value="{t}".format(
        t=pokeData.p_types), inline=True)
    embd.add_field(name="Ability(s)", value="{a}".format(
        a=pokeData.p_abilities), inline=True)

    stats_string = "**HP** : {hp} | **ATK** : {atk} | **DEF** : {df} \n".format(
        hp=pokeData.p_stats["hp"], atk=pokeData.p_stats["attack"], df=pokeData.p_stats["defense"])
    stats_string += "**SPAT** : {spat} | **SPDF** : {spdf} | **SPD** : {spd}".format(
        spat=pokeData.p_stats["special-attack"], spdf=pokeData.p_stats["special-defense"], spd=pokeData.p_stats["speed"])
    embd.add_field(name="Stats", value=stats_string, inline=False)

    embd.description = description
    embd.set_image(url=pokeData.image_link)

    return embd

# get invite embed


def get_invite_embed(embd, color):
    invite_link = global_vars.INVITE_LINK
    thumbnail_link = global_vars.AVATAR_LINK

    embd.title = "Invite Aerial Ace to your server"
    embd.description = "[Click the link and select the server to add to.]({link})".format(
        link=invite_link)
    embd.set_thumbnail(url=thumbnail_link)
    embd.color = color

    return embd
