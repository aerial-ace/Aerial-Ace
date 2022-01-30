import random
from turtle import heading
import discord

import config

links = {
    "kill" : {
        "Good Job {user}, you killed {target}" : "https://i.imgur.com/blvCv4k.gif",
        "{user} ~~crushed~~ killed {target}" : "https://i.imgur.com/NNYGnLe.gif"
    },
    "hit" : {
        "{user} tried hitting {target} but got nerfed, LMAO" : "https://i.imgur.com/Xg0zYp7.gif",
        "{user} slapped {target}, Nicely Done O.O" : "https://i.imgur.com/vF3Lr8v.gif",
        "{user} punched {target}, :100:/:100:" : "https://i.imgur.com/d8p2sms.gif",
        "{user} is hitting {target}, others are enjoying" : "https://i.imgur.com/jqKDrMX.gif",
        "{user} is hitting {target} and i am recording it" : "https://i.imgur.com/Vey97DY.gif",
        "{user} kicked {target}, nice" : "https://i.imgur.com/0uXSS3N.gif",
        "{user} => {target} + punch" : "https://i.imgur.com/KNX3dOA.gif"
    },
    "tease" : {
        "{user} is teasing {target}" : "https://i.imgur.com/gQ6Vbbd.gif",
        "{target} got teased by {user}" : "https://i.imgur.com/BGMXdoR.gif",
        "What are doing {user}? OH, teasing {target}. OK" : "https://i.imgur.com/0wM1PNA.gif"
    },
    "single-dance" : {
        "{user} is dancing. Epik" : "https://i.imgur.com/vYnArw3.gif",
        "Nice dance by {user}" : "https://i.imgur.com/NA085GN.gif",
        "Thats some awesome footwork, {user}" : "https://i.imgur.com/xVHkKXJ.gif",
        "Nice Dance, {user}" : "https://i.imgur.com/T8ZhxqK.gif",
        "Epik dance by {user}" : "https://i.imgur.com/fnXkgsb.gif"
    },
    "double-dance":{
        "{user} is dancing with {target}" : "https://i.imgur.com/nGHoCJW.gif",
        "{target} is dancing with {user}" : "https://i.imgur.com/xbDs4cq.gif",
        "{user} and {target} are dancing, Cool" : "https://i.imgur.com/u2u0tPC.gif"
    },
    "pat" : {
        "{user} pets {target}" : "https://i.imgur.com/NUA66SL.gif",
        "OH, ok" : "https://i.imgur.com/KgjtG5F.gif",
        "{user} pets {target}, 0.0" : "https://i.imgur.com/xmPGH0T.gif",
        "{user} -> pat-pat -> {target}" : "https://i.imgur.com/cYQMCLw.gif"
    }
}

# returns an embed with kill gif
async def get_kill_embed(user_name : str, target_name : str):

    all_headings = list(links["kill"].keys())
    all_links = list(links["kill"].values())

    roll = random.randint(0, len(all_headings) - 1)

    heading = all_headings[roll]
    link = all_links[roll]

    embd = discord.Embed(title=heading.format(user=user_name, target=target_name), color=config.NORMAL_COLOR)
    embd.set_image(url=link)

    return embd

# returns an embed with hit gif
async def get_hit_embed(user_name : str, target_name : str):

    all_headings = list(links["hit"].keys())
    all_links = list(links["hit"].values())

    roll = random.randint(0, len(all_headings) - 1)

    heading = all_headings[roll]
    link = all_links[roll]

    embd = discord.Embed(title=heading.format(user=user_name, target=target_name), color=config.NORMAL_COLOR)
    embd.set_image(url=link)

    return embd

async def get_dance_embed(user_name : str, target_name : str = None):

    if target_name is None or target_name == user_name:
        all_headings = list(links["single-dance"].keys())
        all_links = list(links["single-dance"].values())
    else:
        all_headings = list(links["double-dance"].keys())
        all_links = list(links["double-dance"].values())

    roll = random.randint(0, len(all_headings) - 1)

    heading = all_headings[roll]
    link = all_links[roll]

    embd = discord.Embed(title=heading.format(user=user_name, target=target_name), color=config.NORMAL_COLOR)
    embd.set_image(url=link)

    return embd

async def get_pat_embed(user_name : str, target_name : str):

    all_headings = list(links["pat"].keys())
    all_links = list(links["pat"].values())

    roll = random.randint(0, len(all_headings) - 1) 

    heading = all_headings[roll]
    link = all_links[roll]

    embd = discord.Embed(title=heading.format(user=user_name, target=target_name), color=config.NORMAL_COLOR)
    embd.set_image(url=link)

    return embd

async def get_tease_embed(user_name : str, target_name : str):

    all_headings = list(links["tease"].keys())
    all_links = list(links["tease"].values())

    roll = random.randint(0, len(all_headings) - 1) 

    heading = all_headings[roll]
    link = all_links[roll]

    embd = discord.Embed(title=heading.format(user=user_name, target=target_name), color=config.NORMAL_COLOR)
    embd.set_image(url=link)

    return embd
