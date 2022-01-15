from managers import mongo_manager

# register shiny tags
async def register_tag(server_id, user, tag):

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

    server_document = mongo_manager.manager.get_all_data("tags", query)

    details = server_document[0]

    tag_data = details["tags"]
    tags = list(tag_data.keys())
    users = list(tag_data.values())

    old_tag = ""

    for i in range(0, len(users)):
        if str(user.id) in users[i]:
            old_tag = tags[i]
            break

    if old_tag == tag:
        return f"> **{user.name}** is already assigned to `{tag.capitalize()}` tag"

    if old_tag != "":
        # remove user from current tag
        tag_data[old_tag].remove(str(user.id))

        # remove empty tags
        if len(tag_data[old_tag]) <= 0:
            del tag_data[old_tag]

    try:
        users_assigned_to_new_tag = tag_data[tag]
    except:
        tag_data[tag] = []
        users_assigned_to_new_tag = []

    users_assigned_to_new_tag.append(str(user.id))

    tag_data[tag] = users_assigned_to_new_tag 

    updated_data = {"tags" : tag_data}

    mongo_manager.manager.update_all_data("tags", {"server_id" : server_id}, updated_data)

    if old_tag == "":
        return f"> **{user.name}** was assigned to `{tag.capitalize()}` tag"
    else:
        return f"> **{user.name}** was removed from `{old_tag.capitalize()}` and assigned to `{tag.capitalize()}` tag"

# Get shiny tags
async def get_tag_hunters(server_id, tag):
    
    query = {"server_id" : server_id}

    data_cursor = mongo_manager.manager.get_all_data("tags", query)

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
        print(e)

    return hunters    