import discord
from discord.ext import commands

from managers import mongo_manager
import config

# register server in the database
async def register_guild(bot : commands.Bot, guild : discord.Guild):

    """Add empty server data to the database and inform the admins"""

    server_id = str(guild.id)
    server_name = str(guild.name)

    # create empty servers entry
    server_duplicates = await mongo_manager.manager.get_documents_length("servers", {"server_id" : server_id})
    
    if server_duplicates <= 0:
        entry = {
            "server_id" : server_id, 
            "server_name" : server_name, 
            "starboard" : "0",
            "auto_battle_logging" : "0"
        }
        await mongo_manager.manager.add_data("servers", entry)

    # Log it in support server
    log_channel : discord.TextChannel = bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SERVER_JOIN_LOG_CHANNEL_ID)

    embed = discord.Embed(title="Server Added <:yay_yay:932361191928500284>", color=discord.Color.green())
    embed.add_field(
        name="Server Name",
        value=guild.name,
        inline=True
    )
    embed.add_field(
        name="Member Count",
        value=guild.member_count,
        inline=True
    )
    embed.add_field(
        name="Server Count",
        value=len(bot.guilds),
        inline=False
    )

    await log_channel.send(embed=embed)

    data = {
        "server_id" : server_id,
        "server_name" : "NONE",
        "starboard" : "0"
    }

    return data

async def register_guild_for_battles(guild_id:str):

    # create empty battle entry
    server_duplicates = await mongo_manager.manager.get_documents_length("battles", {"server_id" : guild_id})

    if server_duplicates <= 0:
        entry = {"server_id" : guild_id, "logs" : {}}
        await mongo_manager.manager.add_data("battles", entry)

    return {
        "server_id" : guild_id,
        "logs" : {}
    }

async def register_guild_for_tags(guild_id:str):

    # create empty tags entry
    server_duplicates = await mongo_manager.manager.get_documents_length("tags", {"server_id" : guild_id})

    if server_duplicates <= 0:
        entry = {"server_id" : guild_id, "tags" : {}, "timer" : 0}
        await mongo_manager.manager.add_data("tags", entry)

    return {
        "server_id" : guild_id,
        "tags" : {},
        "timer" : {}
    }

# register guild in the database without other bullshit

async def register_guild_without_bs(guild_id:str, guild_name:str="NONE"):

    server_id = str(guild_id)
    server_name = str(guild_name)

    # create empty servers entry
    server_duplicates = await mongo_manager.manager.get_documents_length("servers", {"server_id" : server_id})
    
    if server_duplicates <= 0:
        entry = {"server_id" : server_id, "server_name" : server_name, "starboard" : "0"}
        await mongo_manager.manager.add_data("servers", entry)

    data = {
        "server_id" : server_id,
        "server_name" : "NONE",
        "starboard" : "0"
    }

    return data

# remove server from the database
async def remove_guild(bot : commands.Bot, guild : discord.Guild):

    """Remove the server's data from the database and inform the admins"""

    server_id = str(guild.id)

    query = {"server_id" : server_id}

    await mongo_manager.manager.remove_all_data("servers", query)

    await mongo_manager.manager.remove_all_data("tags", query)
     
    await mongo_manager.manager.remove_all_data("battles", query)

    log_channel : discord.TextChannel = bot.get_guild(config.SUPPORT_SERVER_ID).get_channel(config.SERVER_JOIN_LOG_CHANNEL_ID)

    embed = discord.Embed(title="Server Removed <:sedCat:933061761337270292>", color=discord.Color.red())
    embed.add_field(
        name="Server Name",
        value=guild.name,
        inline=True
    )
    embed.add_field(
        name="Member Count",
        value=guild.member_count,
        inline=True
    )
    embed.add_field(
        name="Server Count",
        value=len(bot.guilds),
        inline=False
    )

    await log_channel.send(embed=embed)