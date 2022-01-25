import discord

from managers import mongo_manager
import config

# register server in the database
async def register_guild(bot, guild):

    """Add empty server data to the database and inform the admins"""

    server_id = str(guild.id)
    server_name = str(guild.name)
    prefix = "-aa "

    # create empty servers entry
    server_duplicates = mongo_manager.manager.get_documents_length("servers", {"server_id" : server_id})
    
    if server_duplicates <= 0:
        entry = {"server_id" : server_id, "server_name" : server_name, "prefix" : "-aa "}
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

    # Dm the admins on server joins
    admin_id = int(config.ADMIN_ID)
    admin = bot.get_user(admin_id)
    try:
        await admin.send("Aerial Ace was added to **{server}** :]".format(server=guild.name))
    except discord.Forbidden:
        print(
            "Unable to send message to admins. Btw, Aerial Ace was added to **{server}** :]".format(server=guild.name))

# remove server from the database
async def remove_guild(bot, guild):

    """Remove the server's data from the database and inform the admins"""

    server_id = str(guild.id)

    query = {"server_id" : server_id}

    mongo_manager.manager.remove_all_data("servers", query)

    mongo_manager.manager.remove_all_data("tags", query)

    mongo_manager.manager.remove_all_data("battles", query)

    # Dm the admins on server removal
    admin_id = int(config.ADMIN_ID)
    admin = bot.get_user(admin_id)

    try:
        await admin.send("Aerial Ace was removed from **{server}** :_:".format(server=guild.name))
    except discord.Forbidden:
        print("Unable to send message to the admin. Btw, Aerial Ace was removed from {server} :_:".format(server=guild.name))
