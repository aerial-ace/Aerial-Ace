from discord import Message, Member, Reaction
from discord import AutoShardedBot
from asyncio import TimeoutError

from cog_helpers import battle_helper
import config

async def determine_battle_message(bot:AutoShardedBot, message:Message):

    battle_initiation_keywords = ["{}".format(config.POKETWO_ID), "battle "]

    initiation_content = message.content
        
    if message.content.strip().endswith(">") == False:
        return
    
    initiation_content = initiation_content.replace("<@", "").replace(">", "")

    for keyword in battle_initiation_keywords:
        if keyword not in initiation_content:
            return
        else:
            initiation_content = initiation_content.replace(keyword, "")
        
    challenger_id = message.author.id
    target_id     = int(initiation_content.strip())

    if challenger_id == target_id:
        return

    invitation_message:Message = None
        
    def get_battle_message_from_poketwo(_message:Message):

        if _message.author.id != int(config.POKETWO_ID):
            return False
        
        battle_invitation_keywords = ["Challenging", "battle", "checkmark"]

        for keyword in battle_invitation_keywords:
            if keyword not in _message.content:
                return False
            
        if _message.mentions[0].id != target_id:
            return False

        return True
    
    try:
        invitation_message = await bot.wait_for("message", check=get_battle_message_from_poketwo, timeout=10)

    except TimeoutError as t:
        return
    
    def get_confirmation_on_battle_invitation(reaction:Reaction, user:Member):

        if reaction.emoji != "✅":
            return False

        if reaction.message.id != invitation_message.id:
            return False

        if user.id != target_id:
            return False
        
        return True
        
    try:
        await bot.wait_for("reaction_add", check=get_confirmation_on_battle_invitation, timeout=15)

    except TimeoutError as t:
        return await message.channel.send("> Auto Battle Log Session Timed out! Please accept the battle invitation.")

    else:
        await message.channel.send("> Auto Battle Log Session Started!")

    conclusion_type = None
    winner          = None
    loser           = None

    def get_battle_cancel_message(msg:Message):

        nonlocal conclusion_type

        if msg.author.id != challenger_id and msg.author.id != target_id:
            return False
        
        if "x" not in msg.content.lower() and "cancel" not in msg.content.lower():
            return False 

        battle_cancel_keywords = ["{}".format(config.POKETWO_ID), "battle "]
        
        for keyword in battle_cancel_keywords:
            if keyword not in msg.content:
                return False

        conclusion_type = "CANCEL"

        return True
    
    def get_battle_end_message(msg:Message):

        nonlocal conclusion_type, winner, loser

        if msg.author.id != int(config.POKETWO_ID):
            return False
    
        if "won the battle!" in msg.content:
            winner = int(msg.content.split()[0].removeprefix("<@").removesuffix(">"))
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

        reply = await battle_helper.register_battle_log(message.guild.id, str(winner), str(loser))

        await message.channel.send(reply)
