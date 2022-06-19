import discord

from managers import mongo_manager
import config

# register shiny tags
async def register_tag(server_id, user, tag):

    tag = tag.lower()

    query = {"server_id" : str(server_id)}

    """
    Structure : 
    {
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_id" : ["user_id_1", "user_id_2"]
        }
    }
    """

    server_document = await mongo_manager.manager.get_all_data("tags", query)

    details = server_document[0]

    tag_data = details["tags"]
    tags = list(tag_data.keys())
    users = list(tag_data.values())

    old_tag = ""

    for i in range(0, len(users)):
        if str(user.id) in users[i] or f"/{user.id}" in users[i]:
            old_tag = tags[i]
            break

    if old_tag == tag:
        return f"> **{user.name}** is already assigned to `{tag.capitalize()}` tag"

    if old_tag != "":
        # remove user from current tag
        try:
            # Try to remove non afk user id
            tag_data[old_tag].remove(str(user.id))
        except:
            try:
                # Try to remove afk user id
                tag_data[old_tag].remove(f"/{user.id}")
            except:
                pass
            pass

        # remove empty tags
        if len(tag_data[old_tag]) <= 0:
            del tag_data[old_tag]

    try:
        users_assigned_to_new_tag = tag_data[tag]
    except:
        tag_data[tag] = []
        users_assigned_to_new_tag = []

    if str(user.id) not in users_assigned_to_new_tag:
        users_assigned_to_new_tag.append(str(user.id))

    tag_data[tag] = users_assigned_to_new_tag 

    updated_data = {"tags" : tag_data}

    await mongo_manager.manager.update_all_data("tags", {"server_id" : str(server_id)}, updated_data)

    if old_tag == "":
        return f"> **{user.name}** was assigned to `{tag.capitalize()}` tag"
    else:
        return f"> **{user.name}** was removed from `{old_tag.capitalize()}` and assigned to `{tag.capitalize()}` tag"

# Get shiny tags
async def get_tag_hunters(server_id, tag) -> list:
    
    tag = tag.lower()
    query = {"server_id" : str(server_id)}

    data_cursor = await mongo_manager.manager.get_all_data("tags", query)

    """
    {
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_name" : ["hunter_id_1", "hunter_id_2"]
        }
    }
    """

    tag_data = data_cursor[0]["tags"]

    try:
        hunters = tag_data[tag]
    except Exception as e:
        hunters = None

    return hunters    

# Get show hunters embed
async def get_show_hunters_embd(tag, hunters):

    embd = discord.Embed(color=config.NORMAL_COLOR)
    embd.title = "{tag}".format(tag=tag.capitalize())
    embd.description = f"Users assigned to `{tag.capitalize()}` tag \n\n"

    for i in hunters:
        embd.description += "<@{hunter_id}>\n".format(hunter_id=i.replace("/",""))

    return embd

# remove user from their tag
async def remove_user(server_id, user):
    
    user_id = user.id

    query = {"server_id" : str(server_id)}

    mongo_cursor = await mongo_manager.manager.get_all_data("tags", query)

    """
    {
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_name" : ["hunter_id_1", "hunter_id_2"]
        }
    }
    """

    tag_data = mongo_cursor[0]["tags"]
    tags = list(tag_data.keys())
    users = list(tag_data.values())

    old_tag = ""

    for i in range(0, len(users)):
        if str(user_id) in users[i] or f"/{user_id}" in users[i]:
            old_tag = tags[i]
            break

    if old_tag == "":
        return f"> <@{user_id}> is not assigned to any tag."
    else:
        # remove user from current tag
        try:
            tag_data[old_tag].remove(str(user_id))
        except:
            try:
                tag_data[old_tag].remove(f"/{user_id}")
            except:
                pass
            pass

        # remove empty tags
        if len(tag_data[old_tag]) <= 0:
            del tag_data[old_tag]

    updated_tag = {"tags" : tag_data}

    await mongo_manager.manager.update_all_data("tags", query, updated_tag)

    return f"> <@{user_id}> was removed from `{old_tag.capitalize()}` tag"

# remove user from their tag
async def remove_user_id(server_id, user_id : str):
    
    user_id = str(user_id)

    query = {"server_id" : str(server_id)}

    mongo_cursor = await mongo_manager.manager.get_all_data("tags", query)

    """
    {
        "server_id" : "10000000000000000",
        "tags" : {
            "tag_name" : ["hunter_id_1", "hunter_id_2"]
        }
    }
    """

    tag_data = mongo_cursor[0]["tags"]
    tags = list(tag_data.keys())
    users = list(tag_data.values())

    old_tag = ""

    for i in range(0, len(users)):
        if str(user_id) in users[i] or f"/{user_id}" in users[i]:
            old_tag = tags[i]
            break

    if old_tag == "":
        return f"> <@{user_id}> is not assigned to any tag."
    else:
        # remove user from current tag
        try:
            tag_data[old_tag].remove(str(user_id))
        except:
            try:
                tag_data[old_tag].remove(f"/{user_id}")
            except:
                pass
            pass

        # remove empty tags
        if len(tag_data[old_tag]) <= 0:
            del tag_data[old_tag]

    updated_tag = {"tags" : tag_data}

    await mongo_manager.manager.update_all_data("tags", query, updated_tag)

    return f"> <@{user_id}> was removed from `{old_tag.capitalize()}` tag"

# set the afk status of the user
async def set_afk(server_id : str, user_id : str, state : str):

    query = {"server_id" : server_id}

    mongo_cursor = await mongo_manager.manager.get_all_data("tags", query)

    """
    {
        "server_id" : "00000000000000000",
        "tags" : {
            "tag" : ["user", "user"]
        }
    }
    """

    tag_data = mongo_cursor[0]["tags"]

    tags = list(tag_data.keys())
    users = list(tag_data.values())

    if state == "on":
        current_tag = None

        # get the current tag
        for i in range(0, len(users)):
            if user_id in users[i]:
                current_tag = tags[i]

        if current_tag is None:
            return "> `AFK State` is either already **On** or you are not assigned to any tag"

        tag_data[current_tag].remove(user_id)
        new_user_id = f"/{user_id}"

        tag_data[current_tag].append(new_user_id)

        updated_data = {"tags" : tag_data}

        await mongo_manager.manager.update_all_data("tags", query, updated_data)

        return "> You won't pinged now.."

    else:
        current_tag = None

        # get the current tag
        for i in range(0, len(users)):
            if f"/{user_id}" in users[i]:
                current_tag = tags[i]

        if current_tag is None:
            return "> `AFK State` is either already **Off** or you are not assigned to any tag"

        tag_data[current_tag].remove(f"/{user_id}")
        new_user_id = user_id

        tag_data[current_tag].append(new_user_id)

        updated_data = {"tags" : tag_data}

        await mongo_manager.manager.update_all_data("tags", query, updated_data)

        return "> AFK removed, you will recieve pings now." 

async def get_all_tags_embed(server : discord.Guild) -> discord.Embed:

    embd = discord.Embed(title=f"All Tags in {server.name}", color=config.NORMAL_COLOR)
 
    query = {"server_id" : str(server.id)}

    cursor = await mongo_manager.manager.get_all_data("tags", query)

    data = cursor[0]

    """
    {
        "server_id" : "751076697884852389",
        "tags" : {
            "tag" : ["user", "user"]
        }
    }
    """

    all_tags = data["tags"].keys()

    embd.description = ""

    for tag in all_tags:
        embd.description += f"{tag.capitalize()} - "

    embd.set_footer(text=f"This server has a total of {len(all_tags)} tags.")

    return embd