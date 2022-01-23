import random
import discord

import config

links = {
    "kill" : {
        "Good Job {user}, you killed {target}" : "https://cdn.discordapp.com/attachments/893732055421157396/934774416569679882/giphy-1.gif"
    },
    "hit" : {
        "{user} tried hitting {target} but got nerfed, LMAO" : "https://cdn.discordapp.com/attachments/893732055421157396/934784086973759588/ash-hit-mewtwo.gif",
        "{user} slapped {target}, Nicely Done O.O" : "https://cdn.discordapp.com/attachments/893732055421157396/934790956392267776/froakie-hit.gif",
        "{user} punched {target}, :100:/:100:" : "https://cdn.discordapp.com/attachments/893732055421157396/934793006047981568/e3e.gif",
        "{user} is hitting {target}, others are enjoying" : "https://cdn.discordapp.com/attachments/893732055421157396/934790953011650580/meowth-pokemon.gif",
        "{user} is hitting {target} and i am recording it" : "https://cdn.discordapp.com/attachments/893732055421157396/934790953816977478/0564771d6608409c5ed9f2e182dac44d83282758_hq.gif"
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