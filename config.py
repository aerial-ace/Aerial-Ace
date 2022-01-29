import os
import discord

# Bot data
TOKEN = os.environ["TOKEN"]
TEST_TOKEN = os.environ["TEST_TOKEN"]
ADMIN_ID = os.environ["ADMIN_ID"]
POKETWO_ID = os.environ["POKETWO_ID"]

# Mongo Data
MONGO_URI = os.environ["MONGO"]

# bot links
INVITE_LINK = "https://discord.com/api/oauth2/authorize?client_id=908384747393286174&permissions=277025647680&scope=bot%20applications.commands"
AVATAR_LINK = "https://cdn.discordapp.com/avatars/908384747393286174/312dafe2a71e0338db6f2ef5315899a7.webp"
SUPPORT_SERVER_LINK = "https://discord.gg/4mPdqevgsH"
REPO_LINK = "https://github.com/Devanshu19/Aerial-Ace"
GITHUB_PROFILE_LINK = "https://github.com/Devanshu19/"
VOTE_LINK = "https://top.gg/bot/908384747393286174/"

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

# colors
NORMAL_COLOR = discord.Color.blue()
ERROR_COLOR = discord.Color.red()
WARNING_COLOR = discord.Color.orange()
RARE_CATCH_COLOR = discord.Color.gold()

# Reactions
PIKA_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840026094247976/pika_woo.png"
JIRACHI_WOW = "https://cdn.discordapp.com/attachments/911547825274388511/918840025477681152/jirachi_wow.png"
PIKA_SHOCK = "https://cdn.discordapp.com/attachments/911547825274388511/918840025746137158/pika_shock.png"

TIER_LINK = {
    "rare" : "https://media.discordapp.net/attachments/793689115689353247/854410331988426772/image0.png",
    "mega" : "https://cdn.discordapp.com/attachments/793689115689353247/839748732730998784/image0.png",
    "common" : " https://media.discordapp.net/attachments/839209309371891802/900488066437894144/my-image_271.png https://media.discordapp.net/attachments/839209309371891802/900488066756640888/my-image_2721.png https://media.discordapp.net/attachments/839209309371891802/900488065229942804/my-image_272.png https://media.discordapp.net/attachments/839209309371891802/900488065594826863/my-image_273.png",
    "bug" : "https://media.discordapp.net/attachments/774499540938129429/845692957214375966/image0.png?width=400&height=274",
    "dark" : "https://cdn.discordapp.com/attachments/844211981099335680/857496260150558750/image0.png",
    "dragon" : "https://cdn.discordapp.com/attachments/774499540938129429/859643005312172042/my-image_28.png",
    "electric" : "https://cdn.discordapp.com/attachments/774499540938129429/861608474978549770/my-image_35.png",
    "fairy" : "https://cdn.discordapp.com/attachments/774499540938129429/863030732754255892/my-image_41.png",
    "fighting" : "https://media.discordapp.net/attachments/774499540938129429/872263310127558686/my-image_47.png",
    "fire" : "https://media.discordapp.net/attachments/899753866638266418/900555487437807657/my-image_11.png?width=905&height=473",
    "flying" : "https://media.discordapp.net/attachments/774499540938129429/887928654116552724/my-image.png?width=316&height=300", 
    "ghost" : "https://media.discordapp.net/attachments/718008298837770290/844752635684454460/image0.png",
    "grass" : "https://cdn.discordapp.com/attachments/774499540938129429/863911653825445908/my-image_42.png",
    "ground" : "https://cdn.discordapp.com/attachments/718008298837770290/866929735920254976/my-image_43.png",
    "ice" : "https://media.discordapp.net/attachments/774499540938129429/850456657120591943/my-image_9.png?width=793&height=473",
    "normal" : "https://cdn.discordapp.com/attachments/774499540938129429/854348340823851038/my-image_17.png",
    "poison" : "https://media.discordapp.net/attachments/774499540938129429/846577512356249620/my-image_2.png",
    "psychic" : "https://cdn.discordapp.com/attachments/811873800131575850/857622026856824872/my-image_5.png",
    "rock" : "https://cdn.discordapp.com/attachments/718008298837770290/900550270050787358/my-image_8.png",
    "steel" : "https://cdn.discordapp.com/attachments/793689115689353247/898067479471996978/my-image_7.png",
    "water" : "https://cdn.discordapp.com/attachments/774499540938129429/876979764773126225/my-image_55.png"
}
