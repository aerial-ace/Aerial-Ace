from discord import Guild, Member


from managers import mongo_manager

async def register_account(user_id:str, type:str) -> bool:
    """ Registers an account as main or alt """

    query = {"user_id" : user_id}

    try:

        if await mongo_manager.manager.check_existence("alts", query):

            await mongo_manager.manager.update_all_data("alts", query, updated_data={
                "type" : type
            })

        else:

            new_data = {
                "user_id" : user_id,
                "type" : type,
                "main" : user_id,
                "alts" : []
            }

            await mongo_manager.manager.add_data("alts", new_data)
    
    except:
        return False
    else:
        return True
    

async def set_main(user_id:str, main_id:str) -> int:
    """ Sets the main account and the current account as alt account """

    query = {"user_id" : user_id}

    try:

        if await mongo_manager.manager.check_existence("alts", query):
            
            await mongo_manager.manager.update_all_data("alts", query, updated_data={
                "type" : "alt",
                "main" : main_id,
                "alts" : []
            })

            if await add_alt_to_main(main_id, user_id):
                return 1
            else:
                return 0
        else:
            
            new_data = {
                "user_id" : user_id,
                "type" : "alt",
                "main" : main_id,
                "alts" : []
            }

            await mongo_manager.manager.add_data("alts", new_data)

            if await add_alt_to_main(main_id, user_id):
                return 1
            else:
                return 0
    except:
        return -1
    

async def add_alt_to_main(main_id, alt_id) -> bool:
    """ Adds alt to a main account """

    main_query = {"user_id" : main_id}

    if not await mongo_manager.manager.check_existence("alts", main_query):
        return False

    await mongo_manager.manager.update_all_data("alts", main_query, updated_data={
        f"alts.{alt_id}" : {
            "verified" : False
        }
    })

    return True

async def satisfy_status(user_id, guild:Guild) -> int:
    """ Find and Mark all the alt/main accounts of the current user """

    user_cursor = await mongo_manager.manager.get_one("alts", {"user_id" : str(user_id)})
    server_details = await mongo_manager.manager.get_one("altinfo", {"server_id" : str(guild.id)})

    alt_role = guild.get_role(int(server_details.get("alt_role_id")))
    
    main = user_cursor.get("main")
    alt_accounts = user_cursor.get("alts", {})

    if len(user_cursor.items()) <= 0:
        return {"response_code" : 0} # No alt accounts found.

    accounts_modified = []

    for key, value in alt_accounts.items():

        if value.get("verified") is False:
            continue

        mem:Member = guild.get_member(int(key))

        if mem is None:
            continue      

        await mem.add_roles(alt_role, reason="Alt Role Added as per request from the main account : {}".format(user_id))

        accounts_modified.append(key)

    return {"response_code" : 1, "out" : {"alts" : accounts_modified, "main" : main}} # Everything OK.

async def update_role(server_id, role_id) -> int:
    """ Updates the Server's Alt Role. The Role assigned to alt accounts """

    try:
        await mongo_manager.manager.update_all_data(
            "altinfo",
            {"server_id" : server_id},
            {
                "alt_role_id" : role_id
            }
        )
    except Exception as e:
        return -1 # Error occurred while trying to update values
    else:
        return 1  # Everything OK.
