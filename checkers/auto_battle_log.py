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

        global target_id

        if _message.author.id != int(config.POKETWO_ID):
            return False
        
        battle_invitation_keywords = ["Challenging", "battle", "checkmark"]

        for keyword in battle_invitation_keywords:
            if keyword not in _message.content:
                return False

        target_id = int(_message.content.split()[1].removeprefix("<@").removesuffix(">"))

        return True
    
    try:

        invitation_message = await bot.wait_for("message", check=get_battle_message_from_poketwo, timeout=10)

    except TimeoutError as t:

        return await message.channel.send("Auto Logging Session Ended!")
    
    def get_confirmation_on_battle_invitation(reaction:Reaction, user:Member):

        if reaction.emoji != "✅":
            return False

        if reaction.message.id != invitation_message.id:
            return False

        if user.id != target_id:
            return False
        
        return True
        
    try:

        await bot.wait_for("reaction_add", check=get_confirmation_on_battle_invitation, timeout=30)

    except TimeoutError as t:

        return message.channel.send("Invitation was not accepted! Session Ended!")

    def get_battle_cancel_message(msg:Message):

        if msg.author.id != challenger_id and msg.author.id != target_id:
            return False
        
        if "x" not in msg.content.lower() and "cancel" not in msg.content.lower():
            return False 

        battle_cancel_keywords = ["{}".format(config.POKETWO_ID), "battle "]
        
        for keyword in battle_cancel_keywords:
            if keyword not in msg.content:
                return False 

        print("Battle Cancelled by {}".format(msg.author.id))
        return True
    
    def get_battle_end_message(msg:Message):

        if msg.author.id != int(config.ADMIN_ID):
            return False 
        
        if "won the battle!" not in msg.content:
            return False
        
        winner = int(msg.content.split()[0].removeprefix("<@").removesuffix(">"))
        loser  = (target_id if winner == challenger_id else challenger_id)

        #await message.channel.send("Winner : {}\nLoser : {}".format(winner, loser))
        print("Winner : {}\nLoser : {}".format(winner, loser))
        return True

    def get_battle_conclusion(msg:Message):

        if get_battle_cancel_message(msg) is not False:
            return True
        
        if get_battle_end_message(msg) is not False:
            return True
        
        return False

    try:
        await bot.wait_for("message", check=get_battle_conclusion, timeout=20)
    except TimeoutError as t:
        await message.channel.send("Auto Battle Logging session ended with a timeout.")
    
    print("Session Ended!")
