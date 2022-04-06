from discord import Guild, TextChannel, Embed, User
import datetime

from config import SUGGESTION_LOG_CHANNEL_ID, NORMAL_COLOR

async def send_suggestion(guild:Guild, user:User, message:str):

    try:
        suggestion_channel:TextChannel = guild.get_channel(SUGGESTION_LOG_CHANNEL_ID)

        embd = Embed(title="Suggestion Recieved", color=NORMAL_COLOR)
        embd.add_field(
            name="Sent By",
            value=user.name,
            inline=False
        )
        embd.add_field(
            name="Sent From",
            value=guild.name,
            inline=False
        )
        embd.add_field(
            name="Suggestion",
            value=message,
            inline=False
        )

        embd.timestamp = datetime.datetime.now()

        await suggestion_channel.send(embed=embd)
    except Exception as e:
        return f"Error occured while trying to send suggestion \n**ERROR :** {e}"
    else:
        return f"Suggestion sent successfully! Thanks so much for your time :]"

