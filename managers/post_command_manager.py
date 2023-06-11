from discord.ext import commands
from discord import Embed
import random

from views.ButtonViews import DonationView
from cogs import mail as mail_manager
from cogs import tips as tip_manager
import config

async def donation_reminder(ctx:commands.Context):
    
    # Probability that donation embed will be sent after a command execution.
    DONATION_PROB = 10

    roll = random.randint(0, 100)

    if roll <= DONATION_PROB:

        embd = Embed(
            title="Support Aerial Ace",
            color=config.NORMAL_COLOR,
            description="Support the development of Aerial Ace financially by becoming a patron in exchange for various perks. Use `-aa donate` command to check details."
        )

        view = DonationView(600)

        await ctx.send(embed=embd, view=view)

async def process_post_commands(ctx:commands.Context):

    mail_reminder_probability = 30
    tip_reminder_probability  = 50

    if random.randrange(1, 100) < mail_reminder_probability:
        await mail_manager.process_mail(ctx)
    elif random.randint(1, 100) < tip_reminder_probability:
        await tip_manager.TipsModule.send_random_tip(ctx.channel)