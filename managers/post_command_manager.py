from discord.ext import commands
from discord import Embed
import random

from cogs import mail as mail_manager
from views.ButtonViews import DonationView
import config

async def donation_reminder(ctx:commands.Context):
    
    DONATION_PROB = 85

    roll = random.randint(0, 100)

    if roll <= DONATION_PROB:

        embd = Embed(
            title="Support Aerial Ace",
            color=config.NORMAL_COLOR,
            description="Support the development of Aerial Ace financially by becoming a patron in exchange for various perks. Currently, aerial ace is backed by its own developers, you can donate / become a patron to help reduce financial load on them and get some perks in return."
        )

        view = DonationView(600)

        await ctx.send(embed=embd, view=view)

async def process_post_commands(ctx:commands.Context):

    await donation_reminder(ctx)
    await mail_manager.process_mail(ctx)
