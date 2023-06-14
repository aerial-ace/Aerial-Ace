from discord import Message, Member, Reaction
from discord import AutoShardedBot
from asyncio import TimeoutError

from managers import mongo_manager
from helpers import battle_helper
import config

async def determine_battle_message(bot:AutoShardedBot, message:Message):

    initiation_content = message.content

    if not initiation_content.strip().startswith(f"<@{config.POKETWO_ID}>"):
        return
    else:
        initiation_content = initiation_content.removeprefix(f"<@{config.POKETWO_ID}>")

    if message.content.strip().endswith(">") == False:
        return
        
    initiation_content = initiation_content.replace("<@", "").replace(">", "").replace("&", "")
    
    battle_initiation_keywords = ["duel ", "battle "]

    for keyword in battle_initiation_keywords:
        if keyword in initiation_content:
            initiation_content = initiation_content.replace(keyword, "")
            break
    else:
        return

    # Check whether this server has Auto Battle Logging Enabled or Not.
    data_cursor = await mongo_manager.manager.get_all_data("servers", {"server_id" : str(message.guild.id)})
    
    if len(data_cursor) <= 0:
        print(">>>> server_id : {}".format(message.guild.id))

    if data_cursor[0].get("auto_battle_log", 1) != 1:
        return
        
    challenger_id = message.author.id
    challenger_name = message.author.name
    target_id     = int(initiation_content.strip())
    target_name = ""

    if challenger_id == target_id:
        return
    
    def get_confirmation_on_battle_invitation(reaction:Reaction, user:Member):

        nonlocal target_name

        msg:Message = reaction.message

        if msg.author.id != int(config.POKETWO_ID):
            return False
        
        battle_invitation_keywords = ["Challenging", "battle", "checkmark"]

        for keyword in battle_invitation_keywords:
            if keyword not in msg.content:
                return False
            
        if msg.mentions[0].id != target_id:
            return False

        if reaction.emoji != "✅":
            return False

        if user.id != target_id:
            return False
        
        target_name = user.name
        
        return True
        
    try:
        await bot.wait_for("reaction_add", check=get_confirmation_on_battle_invitation, timeout=20)

    except TimeoutError as t:
        return await message.channel.send("> Auto Battle Log Session Timed out! Please accept the battle invitation.")

    else:
        await message.channel.send("> Auto Battle Log Session Started! This will Automatically log the battle results into the battle leaderboard. If you don't want this functionality, use `-aa abl` to Disable this module!\n> **This feature is still in beta!**")

    conclusion_type = None
    winner          = None
    loser           = None

    def get_battle_cancel_message(msg:Message):

        nonlocal conclusion_type

        if not msg.content.strip().startswith(f"<@{config.POKETWO_ID}>"):
            return False

        if msg.author.id != challenger_id and msg.author.id != target_id:
            return False
        
        if "x" not in msg.content.lower() and "cancel" not in msg.content.lower():
            return False 

        battle_cancel_keywords = ["duel ", "battle "]
        
        for keyword in battle_cancel_keywords:
            if keyword in msg.content:
                break
        else:
            return

        conclusion_type = "CANCEL"

        return True
    
    def get_battle_end_message(msg:Message):

        nonlocal conclusion_type, winner, loser

        if msg.author.id != int(config.POKETWO_ID):
            return False
    
        if "won the battle!" in msg.content:
            winner = msg.mentions[0].id
        else:
            if "has won." in msg.content:
                winner = int(msg.content.removesuffix("> has won.").split()[-1].removeprefix("<@"))
            else:
                return False
        
        if winner != challenger_id and winner != target_id:
            return False
        
        conclusion_type = "FINISH"
        
        loser  = (target_id if winner == challenger_id else challenger_id)

        return True

    def get_battle_conclusion(msg:Message):

        if get_battle_cancel_message(msg) is not False:
            return True
        
        if get_battle_end_message(msg) is not False:
            return True
        
        return False

    try:
        await bot.wait_for("message", check=get_battle_conclusion, timeout=10*60)

    except TimeoutError:
        await message.channel.send("> Auto Battle Logging session ended with a timeout. Make sure to register your battle manually.")

    if conclusion_type == "CANCEL":
        return await message.channel.send("> Auto Log Session Cancelled!")
    
    elif conclusion_type == "FINISH":
        await message.channel.send("> Logging Battle. Please Wait!")

        winner_name = (challenger_name if challenger_id == winner else target_name)
        loser_name  = (challenger_name if challenger_id == loser else target_name)

        reply = await battle_helper.register_battle_log(message.guild.id, str(winner), str(loser), winner_name, loser_name)

        await message.channel.send(reply)
