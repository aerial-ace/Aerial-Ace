import os
from dotenv import load_dotenv

load_dotenv()

# Bot data
TOKEN = os.environ["TOKEN"]
TEST_TOKEN = os.environ["TEST_TOKEN"]
ADMIN_ID = "734754644286504991"
POKETWO_ID = "716390085896962058"

MAX_TAG_TIMER_VALUE = 500

TRADE_ITEM_WEIGHT = {
    "pokecoins": 1,
    "shinies": 50000,
    "rares": 5000,
    "redeems": 40000
}

ALERT_TYPE_MASK = {
    "rare" : 0b00001,
    "shiny" : 0b00010,
    "gmax" : 0b00100,
    "hunt" : 0b01000,
    "streak" : 0b10000
}

# Mongo Data
MONGO_URI = os.environ["MONGO"]

# Logging details
SUPPORT_SERVER_ID = 751076697884852389
SERVER_JOIN_LOG_CHANNEL_ID = 938032583726497812
SUGGESTION_LOG_CHANNEL_ID = 938352848448659466

# bot links
DEVELOPER_PROFILE_LINK = "https://discordapp.com/users/734754644286504991"
INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=908384747393286174&permissions=277025647680&scope=bot%20applications.commands"
AVATAR_LINK = "https://i.imgur.com/TAWr46v.png"
SUPPORT_SERVER_LINK = "https://discord.gg/ZpBttKAHwg"
REPO_LINK = "https://github.com/aerial-ace/Aerial-Ace/"
GITHUB_PROFILE_LINK = "https://github.com/Devanshu19/"
VOTE_LINK = "https://top.gg/bot/908384747393286174/vote/"

PATREON_LINK = "https://www.patreon.com/aerial_ace?fan_landing=true"
PAYPAL_LINK = "https://www.paypal.me/devgame19"
KO_FI_LINK = "https://ko-fi.com/aerial_ace"
GITHUB_SPONSORS_LINK = "https://github.com/sponsors/aerial-ace"

# Images
PREMIUM_IMAGE = "https://i.imgur.com/su0fQdJ.png"

# Emojis
AERIAL_ACE_EMOJI = "<:aalogo:1089238103975268433>"
BULLET_EMOJI = "<:bullet:1263187691344887829>"
SUB_SECTION_EMOJI = "<:CA2:1081449816271360040>"
IMPORTANT_EMOJI = "<a:Important:940582149797601391>"
ALERT_EMOJI = "<:alert:940589741714317332>"
ACCEPTED_EMOJI = "<:accepted:1138760940947525702>"
INFO_EMOJI = "<:EG3:1080978835081805904>"
GMAX_EMOJI = "<:gigantamax:1254519073144832124>"
STREAK_EMOJI = "<:upgrades:1043145357070176407>"
LOW_IV_EMOJI = "<:dragon_scale:1237580132005314592>"
HIGH_IV_EMOJI = "<:deep_sea_tooth:1237580253614964736>"
COIN_HEADS_EMOJI = "<:heads:946027174526353448>"
COIN_TAILS_EMOJI = "<:tails:946027156985757746>"
DEVELOPER_EMOJI = "<:developer:956852544666206238>"
NEXT_EMOJI = "<:next:964507779765272648>"
PREV_EMOJI = "<:prev:964508551915634768>"
FIRST_EMOJI = "<:first:964508851166646272>"
LAST_EMOJI = "<:last:964508277809496125>"
PAYPAL_EMOJI = "<:paypal:999716748712480848>"
PATREON_EMOJI = "<:Patreon:999717040057237634>"
KO_FI_EMOJI = "<:kofi:1082687243052921012>"
GITHUB_EMOJI = "<:github:1035069645763383307>"
PREMIUM_EMOJI = "<:premium:1082653563571941438>"
FILLED_START_EMOJI = "<a:loading1:1163072852686274630>"
FILLED_INTERMEDIATE_EMOJI = "<a:loading2:1163072801629016194>"
FILLED_END_EMOJI = "<a:loading3:1163072635723337818>"
EMPTY_START_EMOJI = "<:EmptyStart:1163076164823289987>"
EMPTY_MIDDLE_EMOJI = "<:EmptyMiddle:1163076160633196564>"
EMPTY_END_EMOJI = "<:EmptyEnd:1163076156396933140>"
FILLED_MID_EMOJI = "<a:FilledMiddle:1163086257908367410>"

TYPES = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

# Dex links
NON_SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5/{pokemon}.png"
HIGH_RES_NON_SHINY_LINK_TEMPLATE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon}.png"
SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5-shiny/{pokemon}.png"
HIGH_RES_SHINY_LINK_TEMPLATE = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{pokemon}.png"
POKEMON_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/pokemon/{pokemon}/"
ABILITY_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/abilities/{ability}/"
SMOGON_API_TEMPLATE = "https://smogon-usage-stats.herokuapp.com/gen{gen}{tier}/{pokemon}"
USER_PROFILE_TEMPLATE = "https://discord.com/users/{user_id}"

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
NORMAL_COLOR         = 0x2B2D31
DEFAULT_COLOR        = 0x546e7a
ERROR_COLOR          = 0xe74c3c
WARNING_COLOR        = 0xe67e22
RARE_CATCH_COLOR     = 0x2B2D31
SHINY_CATCH_COLOR    = 0xf1c40f
SMOGON_COLOR         = 0x9b59b6
STREAK_COLOR         = 0xc3f717
LOW_IV_COLOR         = 0xcf65fc
HIGH_IV_COLOR        = 0x71368A
HUNT_COMPLETED_COLOR = 0xc27c0e
GMAX_CATCH_COLOR     = 0xed4245

# starboard defaults
DEFAULT_RARE_TEXT = "{ping} caught a level {level} `{pokemon}` \n\n:tada: Congratulations :tada:\n"
DEFAULT_SHINY_TEXT = "{ping} caught a level {level} **SHINY** `{pokemon}` \n\n :tada: Congratulations :tada:\n"
DEFAULT_GMAX_TEXT = "{ping} caught a level {level} GMAX `{pokemon}` \n\n:tada: Congratulations :tada:\n"

# Reactions
PIKA_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840026094247976/pika_woo.png"
JIRACHI_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840025477681152/jirachi_wow.png"
PIKA_SHOCK = "https://cdn.discordapp.com/attachments/911547825274388511/918840025746137158/pika_shock.png"
NO_IMAGE = "https://i.imgur.com/avAapuP.png"

TIER_LINK = {
    "rare": "https://i.imgur.com/TAbPWeK.png",
    "mega": "https://i.imgur.com/aEkh8Mm.png",
    "common": "https://i.imgur.com/NIq1RZK.png https://i.imgur.com/OgrPggn.png https://i.imgur.com/hjr5aXs.png https://i.imgur.com/9M4oQJr.png",
    "bug": "https://i.imgur.com/pFZmJU1.png",
    "dark": "https://i.imgur.com/hZhsfnj.png",
    "dragon": "https://i.imgur.com/xVSeQZg.png",
    "electric": "https://i.imgur.com/Mm9IP3h.png",
    "fairy": "https://i.imgur.com/YzPJHei.png",
    "fighting": "https://i.imgur.com/xPOwt2J.png",
    "fire": "https://i.imgur.com/U0XYNBa.png",
    "flying": "https://i.imgur.com/quWnAgG.png",
    "ghost": "https://i.imgur.com/QqDrOCP.png",
    "grass": "https://i.imgur.com/WbVVPMg.png",
    "ground": "https://i.imgur.com/nJEZuSc.png",
    "ice": "https://i.imgur.com/2JUuEl0.png",
    "normal": "https://i.imgur.com/0V2rQE0.png",
    "poison": "https://i.imgur.com/6hoKTD9.png",
    "psychic": "https://i.imgur.com/Vt64GPz.png",
    "rock": "https://i.imgur.com/2rWh30S.png",
    "steel": "https://i.imgur.com/sV7gaY6.png",
    "water": "https://i.imgur.com/8Xaj0YF.png",
    "eeveelution": "**Beta : ** https://i.imgur.com/WXTPYHv.png"
}
