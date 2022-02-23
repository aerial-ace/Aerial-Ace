import random
from discord import Embed

from managers import cache_manager
from cog_helpers import general_helper
from cog_helpers import pokedex_helper
from config import NORMAL_COLOR, ERROR_COLOR, COIN_HEADS_EMOJI, COIN_TAILS_EMOJI

"""for getting a random pokemon"""

async def get_random_poke():

    rand_pokemon_id = random.randint(1, 898)

    poke = await pokedex_helper.get_poke_by_id(rand_pokemon_id)

    return poke

"""returns the random pokemon embed """

async def get_random_pokemon_embed():

    poke_data = await get_random_poke()

    embd = Embed(color=NORMAL_COLOR)
    embd.title = "**{0} : {1}**".format(poke_data.p_id, poke_data.p_name)

    description = general_helper.wrap_text(40, poke_data.p_info)
    embd.description = description
    embd.add_field(
        name="Region",
        value=f"{poke_data.p_region}",
        inline=True
    )
    embd.add_field(
        name="Rarity",
        value=f"{poke_data.p_rarity}",
        inline=True
    )
    embd.set_image(url=poke_data.image_link)

    return embd
