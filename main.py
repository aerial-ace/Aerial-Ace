import sys

from discord.ext import commands

from bot import AerialAce
from config import TEST_TOKEN, TOKEN
from managers.logging_manager import setup_logging


def main():
    setup_logging()

    bot = AerialAce()

    if len(sys.argv) < 2:
        is_test = False
    else:
        is_test = sys.argv[1].lower() == "true"

    if is_test is False:
        bot.run(TOKEN)
    else:
        bot.run(TEST_TOKEN)


if __name__ == "__main__":
    print("""
          ___            _       _    ___           
         / _ \\          (_)     | |  / _ \\          
        / /_\\ \\ ___ _ __ _  __ _| | / /_\\ \\ ___ ___ 
        |  _  |/ _ \\ '__| |/ _` | | |  _  |/ __/ _ \\
        | | | |  __/ |  | | (_| | | | | | | (_|  __/
        \\_| |_/\\___|_|  |_|\\__,_|_| \\_| |_/\\___\\___|
          
    """)

    main()
