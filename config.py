import os
import discord
from dotenv import load_dotenv

load_dotenv()

# Bot data
TOKEN = os.environ["TOKEN"]
TEST_TOKEN = os.environ["TEST_TOKEN"]
ADMIN_ID = "734754644286504991"
POKETWO_ID = "716390085896962058"

MAX_TAG_TIMER_VALUE = 500

# Mongo Data
MONGO_URI = os.environ["MONGO"]

# Logging details
SUPPORT_SERVER_ID = 751076697884852389
SERVER_JOIN_LOG_CHANNEL_ID = 938032583726497812
SUGGESTION_LOG_CHANNEL_ID = 938352848448659466

# bot links
DEVELOPER_DISCORD_PROFILE_LINK = "https://discordapp.com/users/734754644286504991"
INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=908384747393286174&permissions=277025647680&scope=bot%20applications.commands"
AVATAR_LINK = "https://i.imgur.com/TAWr46v.png"
SUPPORT_SERVER_LINK = "https://discord.gg/4mPdqevgsH"
REPO_LINK = "https://github.com/aerial-ace/Aerial-Ace/"
GITHUB_PROFILE_LINK = "https://github.com/Devanshu19/"
VOTE_LINK = "https://top.gg/bot/908384747393286174/vote/"

PATREON_LINK = "https://www.patreon.com/aerial_ace?fan_landing=true"
PAYPAL_LINK = "https://www.paypal.me/devgame19"
GITHUB_SPONSORS_LINK = "https://github.com/sponsors/aerial-ace"

# Emojis
BULLET_EMOJI = "<a:arrow_arrow:939409283668410381>"
IMPORTANT_EMOJI = "<a:Important:940582149797601391>"
ALERT_EMOJI = "<:alert:940589741714317332>"
STREAK_EMOJI = "<:upgrades:1043145357070176407>"
COIN_HEADS_EMOJI = "<:heads:946027174526353448>"
COIN_TAILS_EMOJI = "<:tails:946027156985757746>"
DEVELOPER_EMOJI = "<:developer:956852544666206238>"
NEXT_EMOJI = "<:next:964507779765272648>"
PREV_EMOJI = "<:prev:964508551915634768>"
FIRST_EMOJI = "<:first:964508851166646272>"
LAST_EMOJI = "<:last:964508277809496125>"
PAYPAL_EMOJI = "<:paypal:999716748712480848>"
PATREON_EMOJI = "<:Patreon:999717040057237634>"
GITHUB_EMOJI = "<:github:1035069645763383307>"

TYPES = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

# Dex links
NON_SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5/{pokemon}.png"
SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5-shiny/{pokemon}.png"
POKEMON_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/pokemon/{pokemon}/"
ABILITY_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/abilities/{ability}/"
SMOGON_API_TEMPLATE = "https://smogon-usage-stats.herokuapp.com/gen{gen}{tier}/{pokemon}"

# file locations
SERVER_FILE_LOCATION = "data/servers.json"
STATS_FILE_LOCATION = "data/stats.json"
FAV_FILE_LOCATION = "data/fav.json"
TAG_FILE_LOCATION = "data/tags.json"
MOVESET_FILE_LOCATION = "data/moveset.json"
BATTLE_LOG_FILE_LOCATION = "data/battle_log.json"
ALT_NAME_FILE_LOCATION = "data/poke_alt_names.json"
RARITY_FILE_LOCATION = "data/poke_rarity.json"
NATURE_FILE_LOCATION = "data/nature.json"
TYPE_FILE_LOCATION = "data/type_data.json"
WEAKNESS_FILE_LOCATION = "data/weakness_data.json"
DUELISH_POKEMON_FILE_LOCATION = "data/duelish_pokemons.json"

# colors
NORMAL_COLOR = discord.Color.dark_theme()
ERROR_COLOR = discord.Color.red()
WARNING_COLOR = discord.Color.orange()
RARE_CATCH_COLOR = discord.Color.gold()
SMOGON_COLOR = discord.Color.purple()
STREAK_COLOR = 0xc3f717

#starboard defaults
DEFAULT_RARE_TEXT = "{ping} caught a level {level} `{pokemon}` \n\n:tada: Congratulations :tada:\n"
DEFAULT_SHINY_TEXT = "{ping} caught a level {level} **SHINY** `{pokemon}` \n\n :tada: Congratulations :tada:\n"

# Reactions
PIKA_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840026094247976/pika_woo.png"
JIRACHI_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840025477681152/jirachi_wow.png"
PIKA_SHOCK = "https://cdn.discordapp.com/attachments/911547825274388511/918840025746137158/pika_shock.png"
NO_IMAGE = "https://i.imgur.com/avAapuP.png"

TIER_LINK = {
    "rare" : "https://i.imgur.com/TAbPWeK.png",
    "mega" : "https://i.imgur.com/aEkh8Mm.png",
    "common" : "https://i.imgur.com/NIq1RZK.png https://i.imgur.com/OgrPggn.png https://i.imgur.com/hjr5aXs.png https://i.imgur.com/9M4oQJr.png",
    "bug" : "https://i.imgur.com/pFZmJU1.png",
    "dark" : "https://i.imgur.com/50fQwp5.png",
    "dragon" : "https://i.imgur.com/xVSeQZg.png",
    "electric" : "https://i.imgur.com/Mm9IP3h.png",
    "fairy" : "https://i.imgur.com/YzPJHei.png",
    "fighting" : "https://i.imgur.com/xPOwt2J.png",
    "fire" : "https://i.imgur.com/HlyLW5I.png",
    "flying" : "https://i.imgur.com/quWnAgG.png", 
    "ghost" : "https://i.imgur.com/YbFC3qr.png",
    "grass" : "https://i.imgur.com/NFszuTb.png",
    "ground" : "https://i.imgur.com/nJEZuSc.png",
    "ice" : "https://i.imgur.com/2JUuEl0.png",
    "normal" : "https://i.imgur.com/z2pXPLb.png",
    "poison" : "https://i.imgur.com/6hoKTD9.png",
    "psychic" : "https://i.imgur.com/MIwNq5V.png",
    "rock" : "https://i.imgur.com/2rWh30S.png",
    "steel" : "https://i.imgur.com/sV7gaY6.png",
    "water" : "https://i.imgur.com/fdUuqg6.png",
    "eeveelution" : "**Beta : ** https://i.imgur.com/WXTPYHv.png"
}
