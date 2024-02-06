from discord.ext import commands
from discord import Embed
import random

from views.ButtonViews import DonationView
from cogs import mail as mail_manager
from cogs import tips as tip_manager
import config


async def donation_reminder(ctx: commands.Context):
    # Sends a support reminder ever so often

    donation_goal_progress_percentage = 43
    
    empty_chunks = [config.EMPTY_START_EMOJI] + [config.EMPTY_MIDDLE_EMOJI] * 8 + [config.EMPTY_END_EMOJI]

    number_of_loading_bar_chunks = int(donation_goal_progress_percentage / 10)

    for i in range(0, number_of_loading_bar_chunks):

        if i == 0:
            empty_chunks[0] = config.FILLED_START_EMOJI 
        elif i == 9:
            empty_chunks[9] = config.FILLED_END_EMOJI
        else:
            if i == number_of_loading_bar_chunks - 1:
                empty_chunks[i] = config.FILLED_MID_EMOJI
            else:
                empty_chunks[i] = config.FILLED_INTERMEDIATE_EMOJI

    embd = Embed(
        title="Help Aerial Ace",
        color=config.NORMAL_COLOR,
        description="Aerial Ace depends on its users to stay alive. \n\nTo keep the bot running smoothly, I could use some support through donations. Every little bit helps! You also get perks for your generosity! \n## Current Progress \n{} {}%".format("".join(empty_chunks), donation_goal_progress_percentage)
    )

    # Yes, I hard coded the link. 
    embd.set_thumbnail(url="https://i.imgur.com/cYQMCLw.gif")

    view = DonationView(600)

    await ctx.send(embed=embd, view=view)


async def process_post_commands(ctx: commands.Context):
    mail_reminder_probability = -1
    tip_reminder_probability = 5
    support_reminder_probability = 10

    if random.randrange(1, 100) < mail_reminder_probability:
        await mail_manager.process_mail(ctx)
    elif random.randint(1, 100) < tip_reminder_probability:
        await tip_manager.TipsModule.send_random_tip(ctx.channel)
    elif random.randint(1, 100) < support_reminder_probability:
        await donation_reminder(ctx)
