import os
import discord

# Bot data
TOKEN = os.environ["TOKEN"]
TEST_TOKEN = os.environ["TEST_TOKEN"]
ADMIN_ID = "734754644286504991"
POKETWO_ID = "716390085896962058"

# Mongo Data
MONGO_URI = os.environ["MONGO"]

# Logging details
SUPPORT_SERVER_ID = 751076697884852389
SERVER_JOIN_LOG_CHANNEL_ID = 938032583726497812
SUGGESTION_LOG_CHANNEL_ID = 938352848448659466

# bot links
INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=908384747393286174&permissions=277025647680&scope=bot%20applications.commands"
AVATAR_LINK = "https://cdn.discordapp.com/avatars/908384747393286174/16ee31af1a88ab05809b1ea3bac3cc8f.png"
SUPPORT_SERVER_LINK = "https://discord.gg/4mPdqevgsH"
REPO_LINK = "https://github.com/aerial-ace/Aerial-Ace/"
GITHUB_PROFILE_LINK = "https://github.com/Devanshu19/"
VOTE_LINK = "https://top.gg/bot/908384747393286174/vote/"

# Emojis
BULLET_EMOJI = "<a:arrow_arrow:939409283668410381>"
IMPORTANT_EMOJI = "<a:Important:940582149797601391>"
THEFK_EMOJI = "<:thefk:929683678890713108>"
ALERT_EMOJI = "<:alert:940589741714317332>"
PLS_EMOJI = ""
COIN_HEADS_EMOJI = "<:heads:946027174526353448>"
COIN_TAILS_EMOJI = "<:tails:946027156985757746>"

TYPES = ["bug", "dark", "dragon", "electric", "fairy", "fighting", "fire", "flying", "ghost", "grass", "ground", "ice", "normal", "poison", "psychic", "rock", "steel", "water"]

# Dex links
NON_SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5/{pokemon}.png"
SHINY_LINK_TEMPLATE = "https://play.pokemonshowdown.com/sprites/gen5-shiny/{pokemon}.png"
POKEMON_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/pokemon/{pokemon}/"
ABILITY_LINK_TEMPLATE_SMOGON = "https://smogon.com/dex/ss/abilities/{ability}/"
SMOGON_API_TEMPLATE = "https://smogon-usage-stats.herokuapp.com/{tier}/{pokemon}"

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
NORMAL_COLOR = discord.Color.blue()
ERROR_COLOR = discord.Color.red()
WARNING_COLOR = discord.Color.orange()
RARE_CATCH_COLOR = discord.Color.gold()
SMOGON_COLOR = discord.Color.purple()

# Reactions
PIKA_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840026094247976/pika_woo.png"
JIRACHI_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840025477681152/jirachi_wow.png"
PIKA_SHOCK = "https://cdn.discordapp.com/attachments/911547825274388511/918840025746137158/pika_shock.png"
NO_IMAGE = "https://i.imgur.com/avAapuP.png"

TIER_LINK = {
    "rare" : "https://media.discordapp.net/attachments/793689115689353247/924912850953195520/IMG_0018.png",
    "mega" : "https://cdn.discordapp.com/attachments/774499540938129429/870761603153416202/my-image_50.png",
    "common" : " https://media.discordapp.net/attachments/839209309371891802/900488066437894144/my-image_271.png https://media.discordapp.net/attachments/839209309371891802/900488066756640888/my-image_2721.png https://media.discordapp.net/attachments/839209309371891802/900488065229942804/my-image_272.png https://media.discordapp.net/attachments/839209309371891802/900488065594826863/my-image_273.png",
    "bug" : "https://media.discordapp.net/attachments/774499540938129429/845692957214375966/image0.png",
    "dark" : "https://cdn.discordapp.com/attachments/918973688932630589/935020376717672448/my-image_6.png",
    "dragon" : "https://cdn.discordapp.com/attachments/793689115689353247/931947498937921596/my-image_3.png",
    "electric" : "https://cdn.discordapp.com/attachments/793689115689353247/868569489938210836/my-image_46.png",
    "fairy" : "https://cdn.discordapp.com/attachments/793689115689353247/936020121900703744/my-image_11.png",
    "fighting" : "https://cdn.discordapp.com/attachments/718008298837770290/901298772783558716/my-image_14.png",
    "fire" : "https://cdn.discordapp.com/attachments/899753866638266418/900555487437807657/my-image_11.png",
    "flying" : "https://cdn.discordapp.com/attachments/774499540938129429/887928654116552724/my-image.png", 
    "ghost" : "https://media.discordapp.net/attachments/718008298837770290/844752635684454460/image0.png",
    "grass" : "https://media.discordapp.net/attachments/793689115689353247/920423300692332564/IMG_9676.png",
    "ground" : "https://cdn.discordapp.com/attachments/718008298837770290/866929735920254976/my-image_43.png",
    "ice" : "https://media.discordapp.net/attachments/774499540938129429/850456657120591943/my-image_9.png",
    "normal" : "https://cdn.discordapp.com/attachments/718008298837770290/896314513895329853/my-image_1.png",
    "poison" : "https://cdn.discordapp.com/attachments/718008298837770290/934966138415239198/my-image_4.png",
    "psychic" : "https://cdn.discordapp.com/attachments/877212831240560752/909264788935311360/my-image_17.png",
    "rock" : "https://cdn.discordapp.com/attachments/718008298837770290/900550270050787358/my-image_8.png",
    "steel" : "https://cdn.discordapp.com/attachments/918973688932630589/935029992541278208/my-image_8.png",
    "water" : "https://cdn.discordapp.com/attachments/774499540938129429/876979764773126225/my-image_55.png"
}
