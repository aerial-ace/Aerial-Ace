import datetime
import random

from discord import ApplicationContext, Embed, TextChannel, Thread
from discord.abc import GuildChannel, PrivateChannel
from discord.ext import commands

from config import NORMAL_COLOR, SUGGESTION_LOG_CHANNEL_ID
from helpers import general_helper


async def send_suggestion(ctx: commands.Context | ApplicationContext, message: str):
    try:
        suggestion_channel: GuildChannel | PrivateChannel | Thread | None = await general_helper.get_channel_from_bot(ctx.bot, SUGGESTION_LOG_CHANNEL_ID)
        if suggestion_channel is None:
            ref_num: int = random.getrandbits(64)
            return await ctx.send(f"Suggestion not sent! Reference Number : {ref_num}. Please report this at official server")

        embd = Embed(title="Suggestion Recieved", color=NORMAL_COLOR)
        embd.add_field(name="Sent By", value=ctx.author.name, inline=False)
        embd.add_field(name="Sent From", value=ctx.guild.name if ctx.guild is not None else "", inline=False)
        embd.add_field(name="Suggestion", value=message, inline=False)

        embd.timestamp = datetime.datetime.now(datetime.timezone.utc)

        if isinstance(suggestion_channel, TextChannel):
            await suggestion_channel.send(embed=embd)

    except Exception as e:  # noqa: BLE001
        return f"Error occurred while trying to send suggestion \n**ERROR :** {e}"
    else:
        return "Suggestion sent successfully! Thanks so much for your time :]"
