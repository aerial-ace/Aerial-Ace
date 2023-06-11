from discord.ext import commands
from discord import TextChannel
import random

from config import INFO_EMOJI


tips = [
    "You can use the /starboard module to log rare pokemon catches in your server.",
    "You can get premium customization and advanced aerial ace features by subscribing to aerial ace patreon. Use </premium:999727265908789408> to know more.",
    "You can customize the starboard embed's looks. Get premium now!",
    "You can log catch-streaks in starboard module as well. Available to all the premium servers.",
    "You can use the auto-battle log module to log win/loss records of every battle in your server. Use </auto-battle-logging:1117326199434256417> to learn more",
    "You can generate random rules for battling and add an extra layer of challenge. Use </random-ruleset:1088587224167231489> to know more",
    "You can generate random teams added challenge in your battles. Use </random-team:978913900005322776> or </random-matchup:978913900005322777> ",
    "You can create tags, assign users to them and ping them for shiny hunts, collections whatever. Use </tag:939844587529326633>, </pingtag:939844589433552896>",
    "You can get the best </stats:939844386425024532>/</moveset:939844387893030933>/</nature:939844389948260382> info for your pokemon and train them to be the best for what they can be.",
    "You can get ability info using </ability:978913900005322774>",
    "You can express yourself with pokemon gifs using various commands like </cry:978913900378587179>, </dance:939545280351731733>, </pat:939845060298674236> etc.",
    "You can log battles(win/loss) manually by using `-aa lb` command and add them to battle leaderboard of your server.",
    "View your server's battle leaderboard using </battle-leaderboard:939844903486259300>. Log battles using `-aa lb` command"
]

class TipsModule(commands.Cog):

    def __init__(self):
        return
    
    async def get_random_tip():
        return random.sample(tips, k=1)[0]    
    
    async def send_random_tip(channel:TextChannel):
        await channel.send(f"{INFO_EMOJI} **Pro Tip :** {random.sample(tips, k=1)[0]}")

def setup(bot:commands.Bot):
    bot.add_cog(TipsModule())