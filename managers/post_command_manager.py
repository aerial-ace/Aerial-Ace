import random

from discord import TextChannel
from discord.errors import Forbidden
from discord.ext import commands

from cogs import mail as mail_manager
from cogs import tips as tip_manager


async def process_post_commands(ctx: commands.Context):
    mail_reminder_probability = 5
    tip_reminder_probability = 5
    support_reminder_probability = 5

    try:
        if random.randrange(1, 100) < mail_reminder_probability:
            await mail_manager.process_mail(ctx)
        elif random.randint(1, 100) < tip_reminder_probability:
            if isinstance(ctx.channel, TextChannel):
                await tip_manager.TipsModule.send_random_tip(ctx.channel)
        elif random.randint(1, 100) < support_reminder_probability:
            await ctx.send("Support the open source development of Aerial Ace. </about:939844901611372564> </support:1546639707839139944>")
    except Forbidden:
        return
