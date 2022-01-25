import random
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