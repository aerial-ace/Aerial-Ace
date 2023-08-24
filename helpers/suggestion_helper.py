from discord import ApplicationContext, TextChannel, Embed
from discord.ext import commands
import datetime

from config import SUGGESTION_LOG_CHANNEL_ID, NORMAL_COLOR


async def send_suggestion(ctx: commands.Context | ApplicationContext, message: str):
    try:
        botto: commands.Bot = ctx.bot
        suggestion_channel: TextChannel = botto.get_channel(SUGGESTION_LOG_CHANNEL_ID)

        embd = Embed(title="Suggestion Recieved", color=NORMAL_COLOR)
        embd.add_field(
            name="Sent By",
            value=ctx.author.name,
            inline=False
        )
        embd.add_field(
            name="Sent From",
            value=ctx.guild.name,
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
        return f"Error occurred while trying to send suggestion \n**ERROR :** {e}"
    else:
        return f"Suggestion sent successfully! Thanks so much for your time :]"
