import discord
from discord.ext import commands

from managers import mongo_manager
import config

# register server in the database
async def register_guild(bot : commands.Bot, guild : discord.Guild):

    """Add empty server data to the database and inform the admins"""

    server_id = str(guild.id)
    server_name = str(guild.name)
    prefix = "-aa "

    # create empty servers entry
    server_duplicates = mongo_manager.manager.get_documents_length("servers", {"server_id" : server_id})
    
    if server_duplicates <= 0:
        entry = {"server_id" : server_id, "server_name" : server_name, "starboard" : "0"}
        mongo_manager.manager.add_data("servers", entry)

    # create empty tags entry
    server_duplicates = mongo_manager.manager.get_documents_length("tags", {"server_id" : server_id})

    if server_duplicates <= 0:
        entry = {"server_id" : server_id, "tags" : {}}
        mongo_manager.manager.add_data("tags", entry)

    # create empty battle entry
    server_duplicates = mongo_manager.manager.get_documents_length("battles", {"server_id" : server_id})

    if server_duplicates <= 0:
        entry = {"server_id" : server_id, "logs" : {}}
        mongo_manager.manager.add_data("battles", entry)

    # Log it in support server
    log_channel : discord.TextChannel = bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SERVER_JOIN_LOG_CHANNEL_ID)

    embed = discord.Embed(title="Server Added <:yay_yay:932361191928500284>", color=discord.Color.green())
    embed.add_field(
        name="Server Name",
        value=guild.name,
        inline=False
    )
    embed.add_field(
        name="Server Count",
        value=len(bot.guilds),
        inline=False
    )

    embed.set_thumbnail(url=config.AVATAR_LINK)

    await log_channel.send(embed=embed)


# remove server from the database
async def remove_guild(bot : commands.Bot, guild : discord.Guild):

    """Remove the server's data from the database and inform the admins"""

    server_id = str(guild.id)

    query = {"server_id" : server_id}

    mongo_manager.manager.remove_all_data("servers", query)

    mongo_manager.manager.remove_all_data("tags", query)

    mongo_manager.manager.remove_all_data("battles", query)

    log_channel : discord.TextChannel = bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SERVER_JOIN_LOG_CHANNEL_ID)

    embed = discord.Embed(title="Server Removed <:sedCat:933061761337270292>", color=discord.Color.red())
    embed.add_field(
        name="Server Name",
        value=guild.name,
        inline=False
    )
    embed.add_field(
        name="Server Count",
        value=len(bot.guilds),
        inline=False
    )

    embed.set_thumbnail(url=config.AVATAR_LINK)

    await log_channel.send(embed=embed)