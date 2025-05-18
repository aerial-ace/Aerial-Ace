import sys
from time import perf_counter
from functools import wraps

import bot
from managers import cache_manager


def main():
    cache_manager.init()

    print("Hello from aerial-ace!")

    print("""
          ___            _       _    ___           
         / _ \          (_)     | |  / _ \          
        / /_\ \ ___ _ __ _  __ _| | / /_\ \ ___ ___ 
        |  _  |/ _ \ '__| |/ _` | | |  _  |/ __/ _ \\
        | | | |  __/ |  | | (_| | | | | | | (_|  __/
        \_| |_/\___|_|  |_|\__,_|_| \_| |_/\___\___|
          
    """)

    if len(sys.argv) < 2:
        is_test = False
    else:
        is_test = True if sys.argv[1].lower() == "true" else False

    bot.init(is_test)


if __name__ == "__main__":
    main()
