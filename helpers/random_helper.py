import random
from discord import Embed

from managers import cache_manager
from helpers import general_helper
from helpers import pokedex_helper
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


"""Returns a list of random duelish pokemons"""


async def get_random_team(tier: str) -> list | None:
    MAX_SCORE = 90  # maximum score of the team
    MAX_TEAM_SIZE = 3  # maximum team size

    current_score = 0  # current team score

    tier_duelish_pokemons = {}
    team = []

    try:
        tier_duelish_pokemons = cache_manager.cached_duelish_data[tier.lower()]
    except KeyError:
        return None

    for i in range(MAX_TEAM_SIZE):
        max_possible_range = int(((MAX_SCORE - current_score) - 10 * (MAX_TEAM_SIZE - 1 - i)) / 10)  # get the maximum tier from which pokemon can be pulled leaving enough room for other Pokémon
        valid_score_tiers = [score * 10 for score in range(1, max_possible_range + 1)]  # get all the valid score tiers based on the maximum tier, so that pokemon drawn from any of these tier leaves enough score for other Pokémon

        if MAX_TEAM_SIZE - i - 1 == 0:
            random_score_tier = max_possible_range * 10  # if this is the last iteration, just pick from the highest tier as only this tier can maintain a perfect score
        else:
            random_score_tier = valid_score_tiers[random.randint(1, max_possible_range) - 1]  # pick a random score tier from all the valid tiers

        random_tier = tier_duelish_pokemons[str(random_score_tier)]  # get the Pokémon of that random tier
        random_pokemon_from_random_tier = random_tier[random.randint(0, len(random_tier) - 1)]  # get a random pokemon from that random tier

        while random_pokemon_from_random_tier + f" - {random_score_tier}" in team:  # if this pokemon is already in the team, then look for another pokemon from the same tier
            random_pokemon_from_random_tier = random_tier[random.randint(0, len(random_tier) - 1)]  # get a random pokemon from that random tier

        team.append(random_pokemon_from_random_tier + " - " + str(random_score_tier))  # add that random pokemon to the team
        current_score = current_score + int(random_score_tier)  # update the score by subtracting the score of the current pokemon

    return team


"""Returns the embed for single random team"""


async def get_random_team_embed(tier: str) -> Embed:
    team = await get_random_team(tier.lower())

    if team is None:
        return await general_helper.get_info_embd("Tier Error!", f"{tier.capitalize()} is not a valid tier, valid tiers include `common`, `mega`, `rare`", color=ERROR_COLOR)

    embd = Embed(title="Random Team", color=NORMAL_COLOR)
    embd.add_field(
        name="Tier",
        value=tier.capitalize(),
        inline=True
    )

    team_str = "\n".join(team)
    embd.add_field(
        name="Team",
        value=team_str,
        inline=True
    )
    embd.add_field(
        name="Note:",
        value="Make your own rules for the case where you don't have any of these pokemons. It can be as simple as generating a new team, to purchasing that pokemon from the market. Whatever both parties agree upon.",
        inline=False
    )

    return embd


"""Returns the embed for Random Matchups"""


async def get_random_matchup_embd(tier: str) -> Embed:
    player_team = await get_random_team(tier.lower())
    opponent_team = await get_random_team(tier.lower())

    if player_team is None or opponent_team is None:
        return await general_helper.get_info_embd("Tier Error!", f"{tier.capitalize()} is not a valid tier, valid tiers include `common`, `mega`, `rare`", color=ERROR_COLOR)

    embd = Embed(title="Random Matchup", color=NORMAL_COLOR)
    embd.description = f"**Tier** : {tier.capitalize()}"

    player_team_str = "\n".join(player_team)
    opponent_team_str = "\n".join(opponent_team)

    embd.add_field(
        name=f"Your Team {COIN_HEADS_EMOJI}",
        value=player_team_str,
        inline=True
    )

    embd.add_field(
        name=f"Opponent Team {COIN_TAILS_EMOJI}",
        value=opponent_team_str,
        inline=True
    )

    roll = random.randint(0, 1)
    coin_face = (f"{COIN_HEADS_EMOJI}" if roll == 0 else f"{COIN_TAILS_EMOJI}")
    priority_user = ("You" if roll == 0 else "Opponent")

    embd.add_field(
        name="Priority",
        value=f"Coin Tossed! {coin_face} it is! {priority_user} will have priority",
        inline=False
    )

    embd.add_field(
        name="Note:",
        value="Make your own rules for the case where you don't have any of these pokemons. It can be as simple as generating a new team, to purchasing that pokemon from the market. Whatever both parties agree upon.",
        inline=False
    )

    return embd
