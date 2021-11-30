import asyncio
import random
import discord
import requests
import json
from textwrap import TextWrapper

from bot import global_vars
from bot import aerialace_data_manager


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

# starts the rich presence cycle
async def start_rich_presence_cycle(client, repeat_time):
    await set_rich_presence(client)
    while True:
        await asyncio.sleep(repeat_time)
        await set_rich_presence(client)

# set rich presence
async def set_rich_presence(client):
    rand = random.randint(1, 3)
    status = discord.Status.online
    if rand == 1:
        playing_game = discord.Game(name="Dev's shitty games")
        await client.change_presence(activity=playing_game, status=status)
    elif rand == 2:
        watching_prefix = discord.Activity(name="prefix: -aa", type=3)
        await client.change_presence(activity=watching_prefix, status=status)
    else:
        listening_prefix = discord.Activity(name="-aa help", type=2)
        await client.change_presence(activity=listening_prefix, status=status)

# for getting the help embed
def get_help_embed(embd, color):
    embd.title = "Aerial Ace Help"
    embd.color = color

    # help fields
    embd.add_field(
        name="Random Pokemon", 
        value="`-aa rp` or `-aa rand_poke`", 
        inline=False
    )
    embd.add_field(
        name="View Dex Entry",
        value="`-aa dex <pokedex id>` or `-aa dex <pokemon name>`",
        inline=False
    )
    embd.add_field(
        name="Rolling", 
        value="`-aa roll` or `-aa roll <upper limit>`", 
        inline=False
    )
    embd.add_field(
        name="Set Favourite Pokemon",
        value="`-aa set_fav <pokemon name>` or `-aa sf <pokemon name>`",
        inline=False
    )
    embd.add_field(
        name="View Favourite Pokemon", 
        value="`-aa fav`", 
        inline=False
    )
    embd.add_field(
        name="Stats Check",
        value="`-aa stats <pokemon>`", 
        inline=False)
    embd.add_field(
        name="Moveset Check",
        value="`-aa moveset <pokemon name>` or `-aa ms <pokemon name>`",
        inline=False,
    )
    embd.add_field(
        name="Tierlists",
        value="`-aa tierlist <tier type>` or `-aa tl <tier type>`",
        inline=False
    )
    embd.add_field(
        name="Add yourself to a tag",
        value="`-aa tag <tag>`",
        inline=False
    )
    embd.add_field(
        name="Ping users assigned to a tag",
        value="`-aa tag_ping <tag>` or `-aa tp <tag>`",
        inline=False
    )
    embd.add_field(
        name="See users assigned to a tag",
        value="`-aa tag_show <tag>` or `-aa ts <tag>`",
        inline=False
    )
    embd.add_field(
        name="Log Battles",
        value="`-aa log_battle @winner @loser` or `-aa lb @winner @loser`",
        inline=False
    )
    embd.add_field(
        name="See battle score",
        value="`-aa battle_score` or `-aa bs`",
        inline=False
    )
    embd.add_field(
        name="See Battle leaderboard of the server",
        value="`-aa battle_lb` or `-aa blb`",
        inline=False
    )

    return embd


# for getting a pokemon of desired index
def get_poke_by_id(poke_id):

    poke = PokeData()

    general_response = requests.get("https://pokeapi.co/api/v2/pokemon/{0}".format(poke_id))
    data = json.loads(general_response.text)

    species_response = requests.get(
        "https://pokeapi.co/api/v2/pokemon-species/{0}/".format(poke_id)
    )
    species_data = json.loads(species_response.text)

    generation_response = requests.get(
        "https://pokeapi.co/api/v2/generation/{name}/".format(
            name=species_data["generation"]["name"]
        )
    )
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
            poke.p_types += "\n"

    # get_region
    poke.p_region = generation_data["main_region"]["name"].capitalize()

    # get abilities
    abilities = data["abilities"]
    for i in range(0, len(abilities)):
        poke.p_abilities += abilities[i]["ability"]["name"].capitalize()

        if i != len(abilities) - 1:
            poke.p_abilities += "\n"

    # get info
    all_info = species_data["flavor_text_entries"]
    poke.p_info = "*NULL*"

    for i in all_info:
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
def roll(upper_limit):
    roll_value = random.randint(0, upper_limit)
    return roll_value


# get parameter from the message
def get_parameter(msg, removable_command):
    param = msg
    for cmd in removable_command:
        param = param.replace(cmd, "").strip()

    return param


# returns the winner and loser
def get_winner_looser(msg):
    param = get_parameter(msg, ["log_battle", "lb"])
    players = param.split()
    winner, loser = players
    winner, loser = get_id_from_ping(winner), get_id_from_ping(loser)

    return [winner, loser]


# returns user id from ping
def get_id_from_ping(ping):

    user_id = ""
    for i in ping:
        if i.isnumeric():
            user_id = user_id + i

    return user_id

# get random pokemon embed
def get_random_pokemon_embed(embd, poke_data, color, server_id, user_id):

    embd.color = color
    embd.title = "**{0} : {1}**".format(poke_data.p_id, poke_data.p_name)

    description = wrap_text(40, poke_data.p_info)
    embd.description = description
    embd.set_image(url=poke_data.image_link)

    # Ugly, ik '_'
    fav_out = aerialace_data_manager.get_fav(server_id, user_id)
    if fav_out.startswith("> Your favourite pokemon is"):
        fav_poke = (fav_out.replace("> Your favourite pokemon is", "").strip().lower().replace("*", ""))
        if poke_data.p_name.lower() == fav_poke:
            embd.set_footer(text="This pokemon is your favourite")

    return embd


# get Dex entry embed
def get_dex_entry_embed(embd, poke_data, color):
    max_character_width = 40

    embd.color = color
    embd.title = "**{0} : {1}**".format(poke_data.p_id, poke_data.p_name)

    description = wrap_text(max_character_width, poke_data.p_info)
    description += "\n"

    embd.add_field(
        name="Height",
        value="{h} m".format(h=poke_data.p_height),
        inline=True
    )
    embd.add_field(
        name="Weight",
        value="{w} kg".format(w=poke_data.p_weight),
        inline=True
    )
    embd.add_field(
        name="Region",
        value="{r}".format(r=poke_data.p_region),
        inline=True
    )
    embd.add_field(
        name="Type(s)",
        value="{t}".format(t=poke_data.p_types),
        inline=True
    )
    embd.add_field(
        name="Ability(s)",
        value="{a}".format(a=poke_data.p_abilities),
        inline=True
    )
    embd.add_field(
        name="Evolution",
        value="Base State \n Evolved Form",
        inline=True
    )

    stats_string = "**HP** : {hp} | **ATK** : {atk} | **DEF** : {df} \n".format(
        hp=poke_data.p_stats["hp"],
        atk=poke_data.p_stats["attack"],
        df=poke_data.p_stats["defense"],
    )
    stats_string += "**SPAT** : {spat} | **SPDF** : {spdf} | **SPD** : {spd}".format(
        spat=poke_data.p_stats["special-attack"],
        spdf=poke_data.p_stats["special-defense"],
        spd=poke_data.p_stats["speed"],
    )
    embd.add_field(name="Stats", value=stats_string, inline=False)

    embd.description = description
    embd.set_image(url=poke_data.image_link)

    footer_text = "Some pokemon are not searchable by their common names due to the limitation in the api used! Their ids work though."
    embd.set_footer(text=wrap_text(max_character_width, footer_text))

    return embd


# get invite embed
def get_invite_embed(embd, color):
    invite_link = global_vars.INVITE_LINK
    thumbnail_link = global_vars.AVATAR_LINK

    embd.title = "Invite Aerial Ace to your server"
    embd.description = ("[Click the link and select the server to add to.]({link})".format(link=invite_link))
    embd.set_thumbnail(url=thumbnail_link)
    embd.color = color

    return embd


# get battle acceptance
async def get_battle_acceptance(client, message, winner, loser):

    check_id = ""

    if str(message.author.id) == winner:
        check_id = loser
    elif str(message.author.id) == loser:
        check_id = winner
    else:
        await message.channel.send("> Who are you to do this. Let the players log thier battles.")
        return "notapplicable"

    # send battle log request
    log_msg = await message.channel.send("Logging <@{winner}>'s win over <@{loser}>. Click the checkmark to accept."
                                         .format(winner=winner, loser=loser))

    accept_emoji = "☑️"

    await log_msg.add_reaction(accept_emoji)

    def check(_reaction, _user):
        return str(_user.id) == check_id and str(_reaction.emoji) == accept_emoji

    try:
        await client.wait_for("reaction_add", timeout=10.0, check=check)
    except Exception as e:
        return "notaccepted"
    else:
        return "accepted"
