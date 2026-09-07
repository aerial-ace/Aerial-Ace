from discord import Embed

from config import NORMAL_COLOR


async def get_mail_embed() -> Embed:
    embd = Embed(title="__Mail Box - Aerial Ace__", color=NORMAL_COLOR)

    embd.description = "```New```\n"
    embd.description += "PREMIUM FEATURE! Alert Disabling. You can now customize which alerts are shown before logging the catches. If disabled, no alert of that type will be shown but the catch will be logged in the starboard.\n\n To know more, `aa.help starboard`"
    embd.description += "\n\n"

    embd.description += "```Old```\n"
    embd.description += "Separate Logging Channels for Rare and Shiny Pokemons. You can now set a different channel for shiny starboard logs which will allows server owners to showcase the shiny catches in their server in different channels. These channels will only be used for shiny catches and other catches like rare / regional and catch streaks will all be sent to default logging channel like usual. To enable this in your server, use the command `aa.sb shch <shiny_channel>`. For more info, visit the Support Server. \n\n ** ALSO, Low and High IV logs are now open for all servers ( both premium and free servers ). We hope you like this new addition. If you have any suggestions, please let us know. **"

    embd.description += "\n\nThanks for using Aerial Ace as always."

    return embd
